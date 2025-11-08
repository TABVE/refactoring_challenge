from datetime import date

from legacy_code.utils import parse_date


class Forcing:
    """Represents a forcing data point with date (datetime.date), precipitation (in mm), evapotranspiration (in mm), and upstream tracer concentration (in mg/L)."""

    def __init__(
        self,
        date: date,
        precipitation: float,
        evapotranspiration: float,
        upstream_tracer_concentration: float,
    ):
        self.date = date
        self.precipitation = precipitation
        self.evapotranspiration = evapotranspiration
        self.upstream_tracer_concentration = upstream_tracer_concentration


def initialize_forcing(forcing_dicts: list[dict[str, str]]) -> list[Forcing]:
    """Initialize Forcing objects from a list of dictionaries."""
    forcings = []
    for f in forcing_dicts:
        forcings.append(
            Forcing(
                date=parse_date(f["date"]),
                precipitation=float(f.get("precip_mm", 0)),
                evapotranspiration=float(f.get("et_mm", 0)),
                upstream_tracer_concentration=float(f.get("tracer_upstream_mgL", 0)),
            )
        )
    return forcings
