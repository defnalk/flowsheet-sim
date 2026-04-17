"""Distillation API endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.distillation import McCabeThieleRequest, McCabeThieleResponse
from app.solvers.adapter_chemeng import solve_mccabe_thiele

router = APIRouter()


@router.post("/mccabe-thiele/solve", response_model=McCabeThieleResponse)
async def mccabe_thiele_solve(req: McCabeThieleRequest) -> McCabeThieleResponse:
    """Run a McCabe-Thiele binary distillation analysis."""
    try:
        return solve_mccabe_thiele(req)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from None
