"""Pydantic models for reactor endpoints."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, field_validator

from app.models.common import SolverStatus


class ReactorRequest(BaseModel):
    """Request body for POST /api/reactor/solve."""

    reactor_type: Literal["pfr", "cstr", "batch"]
    rate_law_template: str
    rate_law_params: dict[str, float]
    species_names: list[str]
    initial_concentrations: list[float]
    volume_or_time_span: tuple[float, float]
    flow_rate: float | None = None
    reactor_volume: float | None = None
    n_points: int = 200
    key_species: int | None = 0

    @field_validator("initial_concentrations")
    @classmethod
    def non_negative_concentrations(cls, v: list[float]) -> list[float]:
        if any(c < 0 for c in v):
            raise ValueError("Concentrations must be non-negative.")
        return v

    @field_validator("species_names")
    @classmethod
    def at_least_one_species(cls, v: list[str]) -> list[str]:
        if len(v) < 1:
            raise ValueError("At least one species is required.")
        return v


class ReactorResponse(BaseModel):
    """Response body for POST /api/reactor/solve."""

    independent_variable: list[float]
    concentrations: dict[str, list[float]]
    conversion: list[float] | None
    status: SolverStatus
