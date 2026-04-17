"""Component registry API endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.components.registry import get_component, list_components
from app.models.common import ComponentSpec

router = APIRouter()


def _to_spec(c: object) -> ComponentSpec:
    """Convert a ComponentData to the public API model."""
    from app.components.registry import ComponentData

    assert isinstance(c, ComponentData)
    return ComponentSpec(
        name=c.name,
        molecular_weight=c.molecular_weight,
        normal_boiling_point_k=c.normal_boiling_point_k,
        critical_temperature_k=c.Tc_K,
        critical_pressure_pa=c.Pc_Pa,
        acentric_factor=c.acentric_factor,
    )


@router.get("", response_model=list[ComponentSpec])
async def get_all_components() -> list[ComponentSpec]:
    """List all available chemical components."""
    return [_to_spec(c) for c in list_components()]


@router.get("/{name}", response_model=ComponentSpec)
async def get_component_by_name(name: str) -> ComponentSpec:
    """Get a single component by name."""
    try:
        return _to_spec(get_component(name))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None
