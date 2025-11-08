import math
import pytest
from deltares_model.reach import Reach, initialize_reaches

# AI-ASSIST: all written by GitHub Copilot, added type hints manually


def test_reach_defaults_and_attributes() -> None:
    r = Reach(id="A", area_km2=12, tracer_init_mgL=None)
    assert r.id == "A"
    assert isinstance(r.area, float) and r.area == 12.0
    # tracer_init was None -> should default to 0.0
    assert r.tracer_init == 0.0
    # derived/default attributes
    assert r.last_flow_rate == 0.0
    assert r.last_concentration == r.tracer_init
    assert r.run_off == 0.0
    assert math.isnan(r.local_flow_rate)


def test_reach_accepts_string_area_and_nonzero_tracer() -> None:
    # area passed as string should be converted to float
    r = Reach(id="B", area_km2=34.5, tracer_init_mgL=1.23)
    assert r.id == "B"
    assert r.area == 34.5
    assert r.tracer_init == 1.23
    assert r.last_concentration == 1.23


def test_initialize_reaches_success_with_string_inputs_and_zero_tracer() -> None:
    data = [
        {"reach_id": "A", "area_km2": "10", "tracer_init_mgL": "2.5"},
        {"reach_id": "B", "area_km2": "5", "tracer_init_mgL": "0"},
    ]
    reach_a, reach_b = initialize_reaches(data)
    assert isinstance(reach_a, Reach) and isinstance(reach_b, Reach)
    assert (reach_a.id, reach_a.area, reach_a.tracer_init) == ("A", 10.0, 2.5)
    # tracer_init "0" should become 0.0
    assert (reach_b.id, reach_b.area, reach_b.tracer_init) == ("B", 5.0, 0.0)


def test_initialize_reaches_uses_defaults_when_keys_missing() -> None:
    data = [
        {"reach_id": "A"},  # missing area and tracer_init -> defaults to 0.0
        {"reach_id": "B", "area_km2": "3.2"},  # missing tracer_init -> default 0.0
    ]
    a, b = initialize_reaches(data)
    assert a.id == "A" and a.area == 0.0 and a.tracer_init == 0.0
    assert b.id == "B" and b.area == 3.2 and b.tracer_init == 0.0


def test_initialize_reaches_raises_for_invalid_length() -> None:
    with pytest.raises(RuntimeError, match="need exactly 2 reaches A and B"):
        initialize_reaches([{"reach_id": "only_one"}])
    with pytest.raises(RuntimeError, match="need exactly 2 reaches A and B"):
        initialize_reaches([{"reach_id": "a"}, {"reach_id": "b"}, {"reach_id": "c"}])
