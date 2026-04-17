"""Tests for the reactor simulation endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestReactorAPI:
    def test_pfr_first_order(self, client: TestClient) -> None:
        resp = client.post(
            "/api/reactor/solve",
            json={
                "reactor_type": "pfr",
                "rate_law_template": "first_order",
                "rate_law_params": {"k": 0.1},
                "species_names": ["A", "B"],
                "initial_concentrations": [1.0, 0.0],
                "volume_or_time_span": [0, 10],
                "flow_rate": 0.01,
                "n_points": 50,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"]["converged"] is True

        # A should decrease, B should increase
        conc_a = data["concentrations"]["A"]
        conc_b = data["concentrations"]["B"]
        assert conc_a[-1] < conc_a[0]
        assert conc_b[-1] > conc_b[0]

        # Conversion should be between 0 and 1
        assert data["conversion"] is not None
        assert 0.0 < data["conversion"][-1] < 1.0

    def test_cstr_first_order(self, client: TestClient) -> None:
        resp = client.post(
            "/api/reactor/solve",
            json={
                "reactor_type": "cstr",
                "rate_law_template": "first_order",
                "rate_law_params": {"k": 0.1},
                "species_names": ["A", "B"],
                "initial_concentrations": [1.0, 0.0],
                "volume_or_time_span": [0, 10],
                "flow_rate": 0.01,
                "reactor_volume": 10.0,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"]["converged"] is True
        # CSTR returns a single point
        assert len(data["concentrations"]["A"]) == 1

    def test_batch_second_order(self, client: TestClient) -> None:
        resp = client.post(
            "/api/reactor/solve",
            json={
                "reactor_type": "batch",
                "rate_law_template": "second_order",
                "rate_law_params": {"k": 0.05},
                "species_names": ["A", "B"],
                "initial_concentrations": [2.0, 0.0],
                "volume_or_time_span": [0, 50],
                "n_points": 100,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["concentrations"]["A"][-1] < 2.0

    def test_custom_expression(self, client: TestClient) -> None:
        resp = client.post(
            "/api/reactor/solve",
            json={
                "reactor_type": "pfr",
                "rate_law_template": "-k * C[0]; k * C[0]",
                "rate_law_params": {"k": 0.2},
                "species_names": ["S", "P"],
                "initial_concentrations": [1.0, 0.0],
                "volume_or_time_span": [0, 5],
                "flow_rate": 0.01,
                "n_points": 50,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["concentrations"]["S"][-1] < 1.0

    def test_pfr_missing_flow_rate(self, client: TestClient) -> None:
        resp = client.post(
            "/api/reactor/solve",
            json={
                "reactor_type": "pfr",
                "rate_law_template": "first_order",
                "rate_law_params": {"k": 0.1},
                "species_names": ["A", "B"],
                "initial_concentrations": [1.0, 0.0],
                "volume_or_time_span": [0, 10],
            },
        )
        assert resp.status_code == 422

    def test_negative_concentration_rejected(self, client: TestClient) -> None:
        resp = client.post(
            "/api/reactor/solve",
            json={
                "reactor_type": "pfr",
                "rate_law_template": "first_order",
                "rate_law_params": {"k": 0.1},
                "species_names": ["A", "B"],
                "initial_concentrations": [-1.0, 0.0],
                "volume_or_time_span": [0, 10],
                "flow_rate": 0.01,
            },
        )
        assert resp.status_code == 422
