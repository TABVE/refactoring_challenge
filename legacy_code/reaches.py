class Reach:
    """Represents a river reach with an ID, area (in km²), and tracer concentration (in mg/L).
    """
    def __init__(self, id: str, area: float, tracer_concentration: float):
        self.id = id
        self.area_km2 = area
        self.tracer_init_mgL = tracer_concentration