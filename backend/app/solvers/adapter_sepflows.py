"""Adapter layer wrapping sepflows solvers.

Converts between Pydantic request/response models and the sepflows API.
"""

from __future__ import annotations

import numpy as np

from app.models.common import SolverStatus
from app.models.flash import FlashDrumRequest, FlashDrumResponse
from sepflows.flash import FlashDrum


def solve_flash(req: FlashDrumRequest) -> FlashDrumResponse:
    """Run a sepflows isothermal flash calculation."""
    drum = FlashDrum(
        components=req.components,
        temperature_k=req.temperature_k,
        pressure_pa=req.pressure_pa,
    )
    z = np.array(req.feed_mole_fractions, dtype=np.float64)
    result = drum.solve(z)

    components = list(result.components)
    return FlashDrumResponse(
        vapour_fraction=result.vapour_fraction,
        liquid_fraction=result.liquid_fraction,
        liquid_composition=dict(zip(components, result.x.tolist())),
        vapour_composition=dict(zip(components, result.y.tolist())),
        k_values=dict(zip(components, result.k_values.tolist())),
        temperature_k=result.temperature_k,
        pressure_pa=result.pressure_pa,
        status=SolverStatus(converged=result.converged),
    )
