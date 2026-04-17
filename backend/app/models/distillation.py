"""Pydantic models for distillation endpoints."""

from __future__ import annotations

from pydantic import BaseModel, field_validator

from app.models.common import SolverStatus


class McCabeThieleRequest(BaseModel):
    """Request body for POST /api/distillation/mccabe-thiele/solve."""

    alpha: float
    x_D: float = 0.95
    x_B: float = 0.05
    x_F: float = 0.5
    q: float = 1.0
    R: float = 1.5
    max_stages: int = 100

    @field_validator("alpha")
    @classmethod
    def positive_alpha(cls, v: float) -> float:
        if v <= 1.0:
            raise ValueError("Relative volatility alpha must be > 1.0")
        return v

    @field_validator("x_D", "x_B", "x_F")
    @classmethod
    def mole_fraction_range(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError("Mole fraction must be in [0, 1].")
        return v

    @field_validator("R")
    @classmethod
    def positive_reflux(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Reflux ratio must be positive.")
        return v


class McCabeThieleResponse(BaseModel):
    """Response body for POST /api/distillation/mccabe-thiele/solve."""

    n_stages: int
    feed_stage: int
    x_stages: list[float]
    y_stages: list[float]
    diagram_base64: str
    status: SolverStatus
