"""Flash drum API endpoint."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.flash import FlashDrumRequest, FlashDrumResponse
from app.solvers.adapter_sepflows import solve_flash

router = APIRouter()


@router.post("/solve", response_model=FlashDrumResponse)
async def flash_solve(req: FlashDrumRequest) -> FlashDrumResponse:
    """Solve an isothermal flash drum calculation."""
    try:
        return solve_flash(req)
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=422, detail=str(e)) from None
