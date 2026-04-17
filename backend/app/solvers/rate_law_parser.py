"""Safe rate-law expression parser.

Converts user-supplied rate law templates or custom expressions into
Python callables suitable for chemeng.kinetics reactor functions.

Security: custom expressions are parsed via ast and evaluated against
a strict whitelist -- no imports, builtins, or attribute access allowed.
"""

from __future__ import annotations

import ast
import math
from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

# Predefined rate law templates.
# Each returns a function with signature (V_or_t, C) -> rates.
_TEMPLATES: dict[str, str] = {
    "first_order": "A_to_B: r_A = -k * C[0], r_B = k * C[0]",
    "second_order": "A_to_B: r_A = -k * C[0]**2, r_B = k * C[0]**2",
    "reversible_first_order": "A_eq_B: r_A = -kf * C[0] + kr * C[1], r_B = kf * C[0] - kr * C[1]",
    "michaelis_menten": "S_to_P: r_S = -Vmax * C[0] / (Km + C[0]), r_P = Vmax * C[0] / (Km + C[0])",
}

# Functions allowed in custom expressions.
_SAFE_FUNCTIONS: dict[str, Callable[..., float]] = {
    "exp": math.exp,
    "log": math.log,
    "sqrt": math.sqrt,
    "abs": abs,
}

# AST node types permitted in custom expressions.
_ALLOWED_NODES = (
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,
    ast.Name,
    ast.Load,
    ast.Subscript,
    ast.Index,  # Python 3.8 compat, no-op on 3.9+
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.Call,
)


class UnsafeExpressionError(Exception):
    """Raised when a custom expression contains disallowed constructs."""


def _validate_ast(node: ast.AST) -> None:
    """Walk the AST and reject anything outside the whitelist."""
    if not isinstance(node, _ALLOWED_NODES):
        raise UnsafeExpressionError(
            f"Disallowed syntax: {type(node).__name__}. "
            "Only arithmetic, C[i], and safe functions (exp, log, sqrt, abs) are allowed."
        )
    # For Name nodes, allow only 'C' and known safe functions / param names.
    # We can't check param names here (they vary), so we check functions only.
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise UnsafeExpressionError("Only simple function calls are allowed (e.g., exp(...)).")
        if node.func.id not in _SAFE_FUNCTIONS:
            raise UnsafeExpressionError(
                f"Unknown function '{node.func.id}'. "
                f"Allowed: {', '.join(sorted(_SAFE_FUNCTIONS.keys()))}"
            )
    for child in ast.iter_child_nodes(node):
        _validate_ast(child)


def _compile_expression(
    expr: str,
    params: dict[str, float],
) -> Callable[[NDArray[np.float64]], float]:
    """Compile a single safe expression string into a callable.

    The callable takes a concentration vector C and returns a scalar rate.
    """
    tree = ast.parse(expr, mode="eval")
    _validate_ast(tree)
    code = compile(tree, "<rate_law>", "eval")

    namespace: dict[str, object] = {**_SAFE_FUNCTIONS, **params}

    def evaluate(c: NDArray[np.float64]) -> float:
        namespace["C"] = c
        return float(eval(code, {"__builtins__": {}}, namespace))  # noqa: S307

    return evaluate


def parse_rate_law(
    template: str,
    params: dict[str, float],
    n_species: int,
) -> Callable[[float, NDArray[np.float64]], NDArray[np.float64]]:
    """Parse a rate law template or custom expression into a callable.

    Parameters
    ----------
    template
        Either a predefined template name (e.g. ``"first_order"``) or a
        semicolon-separated list of expressions (e.g. ``"-k * C[0]; k * C[0]"``).
    params
        Parameter name-value mapping (e.g. ``{"k": 0.1}``).
    n_species
        Number of species (must match the number of expressions for custom laws).

    Returns
    -------
    callable
        Function with signature ``(V_or_t, C) -> rates`` returning an ndarray
        of shape ``(n_species,)``.
    """
    if template in _TEMPLATES:
        return _build_from_template(template, params, n_species)
    return _build_from_custom(template, params, n_species)


def _build_from_template(
    name: str,
    params: dict[str, float],
    n_species: int,
) -> Callable[[float, NDArray[np.float64]], NDArray[np.float64]]:
    """Build a rate-law callable from a predefined template."""
    spec = _TEMPLATES[name]
    # Extract expressions after the colon, split by comma
    _, rhs = spec.split(":", 1)
    # Each term looks like "r_A = -k * C[0]"
    expressions: list[str] = []
    for term in rhs.split(","):
        _, expr = term.strip().split("=", 1)
        expressions.append(expr.strip())

    if len(expressions) != n_species:
        raise ValueError(
            f"Template '{name}' has {len(expressions)} rate expressions "
            f"but {n_species} species were specified."
        )

    evaluators = [_compile_expression(e, params) for e in expressions]

    def rate_law(_v: float, c: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.array([ev(c) for ev in evaluators], dtype=np.float64)

    return rate_law


def _build_from_custom(
    template: str,
    params: dict[str, float],
    n_species: int,
) -> Callable[[float, NDArray[np.float64]], NDArray[np.float64]]:
    """Build a rate-law callable from semicolon-separated custom expressions."""
    expressions = [e.strip() for e in template.split(";") if e.strip()]

    if len(expressions) != n_species:
        raise ValueError(
            f"Custom rate law has {len(expressions)} expressions "
            f"but {n_species} species were specified."
        )

    evaluators = [_compile_expression(e, params) for e in expressions]

    def rate_law(_v: float, c: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.array([ev(c) for ev in evaluators], dtype=np.float64)

    return rate_law
