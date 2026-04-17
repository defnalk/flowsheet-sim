"""Tests for the safe rate law expression parser."""

from __future__ import annotations

import numpy as np
import pytest

from app.solvers.rate_law_parser import UnsafeExpressionError, parse_rate_law


class TestTemplates:
    def test_first_order(self) -> None:
        fn = parse_rate_law("first_order", {"k": 0.5}, n_species=2)
        c = np.array([2.0, 0.0])
        rates = fn(0.0, c)
        assert rates[0] == pytest.approx(-1.0)
        assert rates[1] == pytest.approx(1.0)

    def test_second_order(self) -> None:
        fn = parse_rate_law("second_order", {"k": 0.1}, n_species=2)
        c = np.array([3.0, 0.0])
        rates = fn(0.0, c)
        assert rates[0] == pytest.approx(-0.9)
        assert rates[1] == pytest.approx(0.9)

    def test_reversible_first_order(self) -> None:
        fn = parse_rate_law("reversible_first_order", {"kf": 1.0, "kr": 0.5}, n_species=2)
        c = np.array([1.0, 1.0])
        rates = fn(0.0, c)
        assert rates[0] == pytest.approx(-0.5)
        assert rates[1] == pytest.approx(0.5)

    def test_michaelis_menten(self) -> None:
        fn = parse_rate_law("michaelis_menten", {"Vmax": 10.0, "Km": 2.0}, n_species=2)
        c = np.array([2.0, 0.0])
        rates = fn(0.0, c)
        assert rates[0] == pytest.approx(-5.0)
        assert rates[1] == pytest.approx(5.0)

    def test_species_count_mismatch(self) -> None:
        with pytest.raises(ValueError, match="species"):
            parse_rate_law("first_order", {"k": 0.1}, n_species=3)


class TestCustomExpressions:
    def test_simple_custom(self) -> None:
        fn = parse_rate_law("-k * C[0]; k * C[0]", {"k": 0.3}, n_species=2)
        c = np.array([4.0, 1.0])
        rates = fn(0.0, c)
        assert rates[0] == pytest.approx(-1.2)
        assert rates[1] == pytest.approx(1.2)

    def test_with_exp(self) -> None:
        fn = parse_rate_law("-exp(-Ea) * C[0]; exp(-Ea) * C[0]", {"Ea": 0.0}, n_species=2)
        c = np.array([1.0, 0.0])
        rates = fn(0.0, c)
        assert rates[0] == pytest.approx(-1.0)

    def test_custom_species_mismatch(self) -> None:
        with pytest.raises(ValueError, match="species"):
            parse_rate_law("-k * C[0]", {"k": 0.1}, n_species=2)


class TestSafety:
    def test_import_blocked(self) -> None:
        with pytest.raises(UnsafeExpressionError):
            parse_rate_law("__import__('os').system('echo hi')", {}, n_species=1)

    def test_attribute_access_blocked(self) -> None:
        with pytest.raises(UnsafeExpressionError):
            parse_rate_law("C[0].__class__", {}, n_species=1)

    def test_unknown_function_blocked(self) -> None:
        with pytest.raises(UnsafeExpressionError):
            parse_rate_law("eval('1+1')", {}, n_species=1)
