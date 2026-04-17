"""Tests for the flash drum endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestFlashAPI:
    def test_methanol_water_flash(self, client: TestClient) -> None:
        resp = client.post(
            "/api/flash/solve",
            json={
                "components": ["methanol", "water"],
                "feed_mole_fractions": [0.5, 0.5],
                "temperature_k": 340.0,
                "pressure_pa": 101325.0,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"]["converged"] is True
        assert 0.0 <= data["vapour_fraction"] <= 1.0
        assert data["liquid_fraction"] == 1.0 - data["vapour_fraction"]

        # Check compositions sum to ~1
        liq = data["liquid_composition"]
        vap = data["vapour_composition"]
        assert abs(sum(liq.values()) - 1.0) < 1e-6
        assert abs(sum(vap.values()) - 1.0) < 1e-6

        # Methanol is more volatile — should be enriched in vapor
        assert vap["methanol"] > liq["methanol"]

    def test_three_component_flash(self, client: TestClient) -> None:
        resp = client.post(
            "/api/flash/solve",
            json={
                "components": ["methanol", "water", "ethanol"],
                "feed_mole_fractions": [0.4, 0.3, 0.3],
                "temperature_k": 350.0,
                "pressure_pa": 101325.0,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"]["converged"] is True
        assert len(data["k_values"]) == 3

    def test_invalid_fractions(self, client: TestClient) -> None:
        resp = client.post(
            "/api/flash/solve",
            json={
                "components": ["methanol", "water"],
                "feed_mole_fractions": [0.3, 0.3],
                "temperature_k": 340.0,
            },
        )
        assert resp.status_code == 422

    def test_single_component_rejected(self, client: TestClient) -> None:
        resp = client.post(
            "/api/flash/solve",
            json={
                "components": ["methanol"],
                "feed_mole_fractions": [1.0],
                "temperature_k": 340.0,
            },
        )
        assert resp.status_code == 422

    def test_unknown_component(self, client: TestClient) -> None:
        resp = client.post(
            "/api/flash/solve",
            json={
                "components": ["methanol", "unobtainium"],
                "feed_mole_fractions": [0.5, 0.5],
                "temperature_k": 340.0,
            },
        )
        assert resp.status_code == 422

    def test_negative_temperature(self, client: TestClient) -> None:
        resp = client.post(
            "/api/flash/solve",
            json={
                "components": ["methanol", "water"],
                "feed_mole_fractions": [0.5, 0.5],
                "temperature_k": -10.0,
            },
        )
        assert resp.status_code == 422
