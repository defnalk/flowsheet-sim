"""Unified chemical component registry.

Merges data from sepflows.constants (Antoine coefficients, critical properties,
molecular weights, boiling points) into a single lookup used by all adapters.
"""

from __future__ import annotations

from dataclasses import dataclass

from sepflows.constants import (
    ANTOINE,
    CRITICAL_PROPERTIES,
    MOLECULAR_WEIGHTS,
    NORMAL_BOILING_POINTS,
)


@dataclass(frozen=True)
class ComponentData:
    """All thermodynamic data for a single component."""

    name: str
    molecular_weight: float
    normal_boiling_point_k: float | None
    Tc_K: float | None
    Pc_Pa: float | None
    acentric_factor: float | None
    antoine_A: float | None
    antoine_B: float | None
    antoine_C: float | None


def _build_registry() -> dict[str, ComponentData]:
    """Build the registry from sepflows constant dictionaries."""
    registry: dict[str, ComponentData] = {}

    all_names = set(MOLECULAR_WEIGHTS.keys())

    for name in sorted(all_names):
        mw = MOLECULAR_WEIGHTS.get(name)
        if mw is None:
            continue

        bp = NORMAL_BOILING_POINTS.get(name)
        crit = CRITICAL_PROPERTIES.get(name, {})
        ant = ANTOINE.get(name, {})

        # sepflows stores Pc in bar; convert to Pa
        pc_bar = crit.get("Pc")
        pc_pa = pc_bar * 1e5 if pc_bar is not None else None

        registry[name] = ComponentData(
            name=name,
            molecular_weight=mw,
            normal_boiling_point_k=bp,
            Tc_K=crit.get("Tc"),
            Pc_Pa=pc_pa,
            acentric_factor=crit.get("omega"),
            antoine_A=ant.get("A"),
            antoine_B=ant.get("B"),
            antoine_C=ant.get("C"),
        )

    return registry


REGISTRY: dict[str, ComponentData] = _build_registry()


def get_component(name: str) -> ComponentData:
    """Look up a component by name, raising KeyError if not found."""
    try:
        return REGISTRY[name]
    except KeyError:
        available = ", ".join(sorted(REGISTRY.keys()))
        raise KeyError(f"Unknown component '{name}'. Available: {available}") from None


def list_components() -> list[ComponentData]:
    """Return all registered components sorted by name."""
    return list(REGISTRY.values())
