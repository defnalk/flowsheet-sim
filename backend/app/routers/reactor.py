"""Reactor simulation API endpoint."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.reactor import ReactorRequest, ReactorResponse
from app.solvers.adapter_chemeng import solve_reactor

router = APIRouter()


@router.post("/solve", response_model=ReactorResponse)
async def reactor_solve(req: ReactorRequest) -> ReactorResponse:
    """Solve a PFR, CSTR, or batch reactor simulation."""
    try:
        return solve_reactor(req)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=422, detail=str(e)) from None
