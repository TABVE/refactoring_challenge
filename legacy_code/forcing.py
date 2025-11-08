from datetime import date

class Forcing:
    """Represents a forcing data point with date (datetime.date), precipitation (in mm), evapotranspiration (in mm), and upstream tracer concentration (in mg/L).
    """
    def __init__(self, date: date, precipitation: float, evapotranspiration: float, upstream_tracer_concentration: float):
        self.date = date
        self.precipitation = precipitation
        self.evapotranspiration = evapotranspiration
        self.upstream_tracer_concentration = upstream_tracer_concentration
