"""Tests for the component registry and API endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.components.registry import REGISTRY, get_component, list_components


class TestRegistry:
    def test_registry_not_empty(self) -> None:
        assert len(REGISTRY) > 0

    def test_methanol_present(self) -> None:
        c = get_component("methanol")
        assert c.name == "methanol"
        assert c.molecular_weight == pytest.approx(32.042)
        assert c.Tc_K is not None
        assert c.Pc_Pa is not None
        # sepflows stores Pc in bar, we convert to Pa
        assert c.Pc_Pa == pytest.approx(80.97e5)

    def test_water_present(self) -> None:
        c = get_component("water")
        assert c.molecular_weight == pytest.approx(18.015)
        assert c.antoine_A is not None

    def test_unknown_component_raises(self) -> None:
        with pytest.raises(KeyError, match="Unknown component"):
            get_component("unobtainium")

    def test_list_components_sorted(self) -> None:
        comps = list_components()
        names = [c.name for c in comps]
        assert names == sorted(names)


class TestComponentsAPI:
    def test_get_all(self, client: TestClient) -> None:
        resp = client.get("/api/components")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 5
        names = {c["name"] for c in data}
        assert "methanol" in names
        assert "water" in names

    def test_get_one(self, client: TestClient) -> None:
        resp = client.get("/api/components/methanol")
        assert resp.status_code == 200
        assert resp.json()["name"] == "methanol"

    def test_get_unknown_404(self, client: TestClient) -> None:
        resp = client.get("/api/components/unobtainium")
        assert resp.status_code == 404


import pytest  # noqa: E402 — already imported via conftest but needed for approx
