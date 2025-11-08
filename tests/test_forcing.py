import pytest
from datetime import date
from legacy_code.forcing import Forcing, initialize_forcing

def test_forcing_initialization():
    # Test basic initialization
    d = date(2023, 1, 1)
    f = Forcing(d, 10.0, 5.0, 2.0)
    assert f.date == d
    assert f.precipitation == 10.0 
    assert f.evapotranspiration == 5.0
    assert f.upstream_tracer_concentration == 2.0

def test_initialize_forcing():
    # Test with complete data
    forcing_dicts = [
        {
            "date": "2023-01-01",
            "precip_mm": "10.0",
            "et_mm": "5.0", 
            "tracer_upstream_mgL": "2.0"
        }
    ]
    forcings = initialize_forcing(forcing_dicts)
    assert len(forcings) == 1
    assert isinstance(forcings[0], Forcing)
    assert forcings[0].date == date(2023, 1, 1)
    assert forcings[0].precipitation == 10.0
    assert forcings[0].evapotranspiration == 5.0
    assert forcings[0].upstream_tracer_concentration == 2.0

def test_initialize_forcing_missing_values():
    # Test with missing optional values
    forcing_dicts = [
        {
            "date": "2023-01-01"
        }
    ]
    forcings = initialize_forcing(forcing_dicts)
    assert len(forcings) == 1
    assert forcings[0].precipitation == 0.0
    assert forcings[0].evapotranspiration == 0.0
    assert forcings[0].upstream_tracer_concentration == 0.0

def test_initialize_forcing_multiple_entries():
    # Test with multiple entries
    forcing_dicts = [
        {
            "date": "2023-01-01",
            "precip_mm": "10.0"
        },
        {
            "date": "2023-01-02",
            "et_mm": "5.0"
        }
    ]
    forcings = initialize_forcing(forcing_dicts)
    assert len(forcings) == 2
    assert forcings[0].date == date(2023, 1, 1)
    assert forcings[1].date == date(2023, 1, 2)