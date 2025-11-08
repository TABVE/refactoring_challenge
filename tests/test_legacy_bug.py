from __future__ import annotations

# Failing regression tests that capture real defects in legacy_code.
# Candidates should fix the bugs during refactor and make these pass (or replace with equivalent tests on src/).

import math
import pytest

# AI-ASSIST: Example marker to illustrate how to annotate AI-influenced code or tests.
from legacy_code import water_model as legacy


@pytest.mark.parametrize(
    "q1,c1,q2,c2",
    [
        (0.0, 1.0, 0.0, 1.0),
        (1.0, 10.0, 3.0, 0.0),
    ],
)
def test_tracer_mixing_should_be_flow_weighted(q1, c1, q2, c2):
    """Test that tracer mixing uses flow-weighted mass balance."""
    # Calculate expected flow-weighted concentration
    if q1 + q2 == 0:
        expected = 0.0
    elif q1 + q2 < 0:
        expected = float("nan")
    else:
        expected = (q1 * c1 + q2 * c2) / (q1 + q2)

    got = legacy.mix_concentration(q1, c1, q2, c2)

    # Intentional failing assertion: legacy uses simple average (5.0) which is wrong.
    assert math.isclose(
        got, expected, rel_tol=1e-9
    ), "Legacy tracer mixing is incorrect; should be flow-weighted mass balance"

@pytest.mark.parametrize(
    "mm_per_day,area_km2,expected",
    [
        (86.4, 1.0, 1.0),  # 1 m^3/s
        (0.0, 1.0, 0.0),   # zero flow
    ],
)
def test_mm_day_to_m3s_conversion_on_1km2_should_be_1_m3s(mm_per_day, area_km2, expected):
    """Test that mm/day to m^3/s conversion is correct for 1 km^2 area."""
    got = legacy.mm_day_to_m3s(mm_per_day, area_km2)

    assert math.isclose(
        got, expected, rel_tol=1e-12
    ), "Legacy unit conversion mm/day -> m^3/s is incorrect"

def test_mm_day_to_m3s_negative_area_should_raise():
    """Test that negative area raises ValueError."""
    with pytest.raises(ValueError):
        legacy.mm_day_to_m3s(100.0, -1.0)