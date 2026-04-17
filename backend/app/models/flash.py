"""Pydantic models for the flash drum endpoint."""

from __future__ import annotations

from pydantic import BaseModel, field_validator

from app.models.common import SolverStatus


class FlashDrumRequest(BaseModel):
    """Request body for POST /api/flash/solve."""

    components: list[str]
    feed_mole_fractions: list[float]
    temperature_k: float
    pressure_pa: float = 101_325.0

    @field_validator("components")
    @classmethod
    def at_least_two_components(cls, v: list[str]) -> list[str]:
        if len(v) < 2:
            raise ValueError("At least two components are required.")
        return v

    @field_validator("feed_mole_fractions")
    @classmethod
    def fractions_sum_to_one(cls, v: list[float]) -> list[float]:
        if abs(sum(v) - 1.0) > 1e-4:
            raise ValueError(f"Mole fractions must sum to 1.0, got {sum(v):.6f}")
        return v

    @field_validator("temperature_k")
    @classmethod
    def positive_temperature(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Temperature must be positive.")
        return v

    @field_validator("pressure_pa")
    @classmethod
    def positive_pressure(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Pressure must be positive.")
        return v


class FlashDrumResponse(BaseModel):
    """Response body for POST /api/flash/solve."""

    vapour_fraction: float
    liquid_fraction: float
    liquid_composition: dict[str, float]
    vapour_composition: dict[str, float]
    k_values: dict[str, float]
    temperature_k: float
    pressure_pa: float
    status: SolverStatus
