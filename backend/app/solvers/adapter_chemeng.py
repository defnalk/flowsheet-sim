"""Adapter layer wrapping chemeng-toolkit solvers.

Converts between Pydantic request/response models and the chemeng API.
"""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from app.models.common import SolverStatus
from app.models.distillation import McCabeThieleRequest, McCabeThieleResponse
from app.models.reactor import ReactorRequest, ReactorResponse
from app.solvers.figure_export import figure_to_base64
from app.solvers.rate_law_parser import parse_rate_law
from chemeng.kinetics import batch_reactor, cstr, pfr
from chemeng.separations import mccabe_thiele

matplotlib.use("Agg")


def solve_mccabe_thiele(req: McCabeThieleRequest) -> McCabeThieleResponse:
    """Run a McCabe-Thiele distillation analysis."""
    result = mccabe_thiele(
        alpha=req.alpha,
        x_D=req.x_D,
        x_B=req.x_B,
        x_F=req.x_F,
        q=req.q,
        R=req.R,
        max_stages=req.max_stages,
    )

    diagram_b64 = figure_to_base64(result.figure)
    plt.close(result.figure)

    return McCabeThieleResponse(
        n_stages=result.n_stages,
        feed_stage=result.feed_stage,
        x_stages=result.x_stages,
        y_stages=result.y_stages,
        diagram_base64=diagram_b64,
        status=SolverStatus(converged=True),
    )


def solve_reactor(req: ReactorRequest) -> ReactorResponse:
    """Run a PFR, CSTR, or batch reactor simulation."""
    c0 = np.array(req.initial_concentrations, dtype=np.float64)
    n_species = len(req.species_names)

    rate_law = parse_rate_law(req.rate_law_template, req.rate_law_params, n_species)

    if req.reactor_type == "pfr":
        if req.flow_rate is None:
            raise ValueError("flow_rate is required for PFR.")
        result = pfr(
            rate_law=rate_law,
            C0=c0,
            V_span=req.volume_or_time_span,
            Q=req.flow_rate,
            n_points=req.n_points,
            key_species=req.key_species,
        )
    elif req.reactor_type == "cstr":
        if req.flow_rate is None:
            raise ValueError("flow_rate is required for CSTR.")
        if req.reactor_volume is None:
            raise ValueError("reactor_volume is required for CSTR.")

        # CSTR rate_law takes only C (no V argument)
        def cstr_rate(c: np.ndarray) -> np.ndarray:  # type: ignore[type-arg]
            return rate_law(0.0, c)

        result = cstr(
            rate_law=cstr_rate,
            C0=c0,
            V=req.reactor_volume,
            Q=req.flow_rate,
            key_species=req.key_species,
        )
    elif req.reactor_type == "batch":
        result = batch_reactor(
            rate_law=rate_law,
            C0=c0,
            t_span=req.volume_or_time_span,
            n_points=req.n_points,
            key_species=req.key_species,
        )
    else:
        raise ValueError(f"Unknown reactor type: {req.reactor_type}")

    concentrations: dict[str, list[float]] = {}
    for i, name in enumerate(req.species_names):
        concentrations[name] = result.concentrations[:, i].tolist()

    conversion = result.conversion.tolist() if result.conversion is not None else None

    return ReactorResponse(
        independent_variable=result.volume_or_time.tolist(),
        concentrations=concentrations,
        conversion=conversion,
        status=SolverStatus(converged=True),
    )
