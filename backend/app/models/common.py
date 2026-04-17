"""Shared Pydantic models used across all endpoints."""

from __future__ import annotations

from pydantic import BaseModel


class SolverStatus(BaseModel):
    """Convergence status returned by every solver endpoint."""

    converged: bool
    iterations: int | None = None
    message: str | None = None


class ComponentSpec(BaseModel):
    """Public representation of a chemical component."""

    name: str
    molecular_weight: float
    normal_boiling_point_k: float | None = None
    critical_temperature_k: float | None = None
    critical_pressure_pa: float | None = None
    acentric_factor: float | None = None
