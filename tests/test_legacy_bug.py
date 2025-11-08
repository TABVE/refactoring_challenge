from __future__ import annotations

import math
import pytest

from deltares_model.water_model import mix_concentration, mm_day_to_m3s


@pytest.mark.parametrize(
    "q1,c1,q2,c2",
    [
        (0.0, 1.0, 0.0, 1.0),
        (1.0, 10.0, 3.0, 0.0),
        (1.0, 10.0, -3.0, 0.0),
        (-3.0, 10.0, -1.0, 0.0),
    ],
)
def test_tracer_mixing_should_be_flow_weighted(
    q1: float, c1: float, q2: float, c2: float
) -> None:
    """Test that tracer mixing uses flow-weighted mass balance."""
    # Calculate expected flow-weighted concentration
    if q1 + q2 == 0:
        expected = 0.0
    elif q1 + q2 < 0:
        expected = float("nan")
    else:
        expected = (q1 * c1 + q2 * c2) / (q1 + q2)

    got = mix_concentration(q1, c1, q2, c2)

    if math.isnan(expected):
        assert math.isnan(
            got
        ), "Legacy tracer mixing is incorrect; should be flow-weighted mass balance"
    else:
        assert math.isclose(
            got, expected, rel_tol=1e-9
        ), "Legacy tracer mixing is incorrect; should be flow-weighted mass balance"


@pytest.mark.parametrize(
    "mm_per_day,area_km2,expected",
    [
        (86.4, 1.0, 1.0),  # 1 m^3/s
        (0.0, 1.0, 0.0),  # zero flow
        (1.0, 0.0, float("nan")),  # zero area -> nan
    ],
)
def test_mm_day_to_m3s_conversion_on_1km2_should_be_1_m3s(
    mm_per_day: float, area_km2: float, expected: float
) -> None:
    """Test that mm/day to m^3/s conversion is correct for 1 km^2 area."""
    got = mm_day_to_m3s(mm_per_day, area_km2)

    if math.isnan(expected):
        assert math.isnan(got), "Legacy unit conversion mm/day -> m^3/s is incorrect"
    else:
        assert math.isclose(
            got, expected, rel_tol=1e-12
        ), "Legacy unit conversion mm/day -> m^3/s is incorrect"


def test_mm_day_to_m3s_negative_area_should_raise() -> None:
    """Test that negative area raises ValueError."""
    with pytest.raises(ValueError):
        mm_day_to_m3s(100.0, -1.0)
