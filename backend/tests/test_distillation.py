"""Tests for the McCabe-Thiele distillation endpoint."""

from __future__ import annotations

import base64

from fastapi.testclient import TestClient


class TestMcCabeThieleAPI:
    def test_basic_distillation(self, client: TestClient) -> None:
        resp = client.post(
            "/api/distillation/mccabe-thiele/solve",
            json={
                "alpha": 2.5,
                "x_D": 0.95,
                "x_B": 0.05,
                "x_F": 0.5,
                "q": 1.0,
                "R": 1.5,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"]["converged"] is True
        assert data["n_stages"] > 0
        assert data["feed_stage"] > 0
        assert data["feed_stage"] <= data["n_stages"]

        # Verify diagram is valid base64-encoded PNG
        png_bytes = base64.b64decode(data["diagram_base64"])
        assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"

    def test_high_alpha_fewer_stages(self, client: TestClient) -> None:
        """Higher relative volatility should require fewer stages."""
        resp_low = client.post(
            "/api/distillation/mccabe-thiele/solve",
            json={"alpha": 2.0, "x_D": 0.90, "x_B": 0.10, "x_F": 0.5, "q": 1.0, "R": 2.0},
        )
        resp_high = client.post(
            "/api/distillation/mccabe-thiele/solve",
            json={"alpha": 5.0, "x_D": 0.90, "x_B": 0.10, "x_F": 0.5, "q": 1.0, "R": 2.0},
        )
        assert resp_low.status_code == 200
        assert resp_high.status_code == 200
        assert resp_high.json()["n_stages"] < resp_low.json()["n_stages"]

    def test_alpha_must_be_gt_one(self, client: TestClient) -> None:
        resp = client.post(
            "/api/distillation/mccabe-thiele/solve",
            json={"alpha": 0.8, "x_D": 0.95, "x_B": 0.05, "x_F": 0.5, "q": 1.0, "R": 1.5},
        )
        assert resp.status_code == 422

    def test_invalid_mole_fraction(self, client: TestClient) -> None:
        resp = client.post(
            "/api/distillation/mccabe-thiele/solve",
            json={"alpha": 2.5, "x_D": 1.5, "x_B": 0.05, "x_F": 0.5, "q": 1.0, "R": 1.5},
        )
        assert resp.status_code == 422

    def test_saturated_vapor_feed(self, client: TestClient) -> None:
        resp = client.post(
            "/api/distillation/mccabe-thiele/solve",
            json={"alpha": 2.5, "x_D": 0.90, "x_B": 0.10, "x_F": 0.5, "q": 0.0, "R": 2.0},
        )
        assert resp.status_code == 200
        assert resp.json()["n_stages"] > 0
