import math
from unittest.mock import patch


from legacy_code.water_model import run_all


@patch("legacy_code.water_model.read_csv_as_dicts")
def test_run_all(mock_read_csv):
    mock_forcing = [
        {
            "date": "2023-01-01",
            "precip_mm": "10.0",
            "et_mm": "2.0", 
            "tracer_upstream_mgL": "1.0"
        },
        {
            "date": "2023-01-02", 
            "precip_mm": "5.0",
            "et_mm": "3.0",
            "tracer_upstream_mgL": "1.5"
        }
    ]
    mock_reaches = [
        {"area_km2": "100", "tracer_init_mgL": "5.0"},
        {"area_km2": "200", "tracer_init_mgL": "2.0"}
    ]
    mock_read_csv.side_effect = [mock_forcing, mock_reaches]
    results = run_all()

    assert len(results) == 4  # 2 dates * 2 reaches
    
    # Check first timestep reach A
    assert results[0]["reach"] == "A"
    assert results[0]["date"] == "2023-01-01"
    assert isinstance(results[0]["q_m3s"], float)
    assert isinstance(results[0]["c_mgL"], float)

    # Check first timestep reach B
    assert results[1]["reach"] == "B" 
    assert results[1]["date"] == "2023-01-01"
    assert isinstance(results[1]["q_m3s"], float)
    assert isinstance(results[1]["c_mgL"], float)

    # Check that Q in B is larger than Q in A (adds local runoff)
    assert results[1]["q_m3s"] > results[0]["q_m3s"]

    mock_read_csv.assert_called()
    
    # In order to refactor check actual values of first timestep, will be removed later
    assert math.isclose(
            results[-1]["c_mgL"], 3.137311847474605, rel_tol=1e-12
        )
    assert math.isclose(
            results[-2]["c_mgL"], 3.6718633402577496, rel_tol=1e-12
        )
    
