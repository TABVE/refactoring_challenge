class Reach:
    """Represents a river reach with an ID, area (in km²), and tracer concentration (in mg/L)."""

    def __init__(
        self, id: str, area_km2: float, tracer_init_mgL: float | None = None
    ):
        self.id = id
        self.area = float(area_km2)
        self.tracer_init = tracer_init_mgL or 0.0
        self.last_flow_rate = 0.0
        self.last_concentration = self.tracer_init
        self.run_off = 0.0  # mm/day
        self.local_flow_rate = float("nan")


def initialize_reaches(reach_dicts: list[dict[str, str]]) -> list[Reach]:
    """Initialize Reach objects from a list of dictionaries."""
    if len(reach_dicts) != 2:
        raise RuntimeError("need exactly 2 reaches A and B")

    reaches = []
    for reach in reach_dicts:
        reaches.append(
            Reach(
                id=reach["reach_id"],
                area_km2=float(reach.get("area_km2", "0")),
                tracer_init_mgL=float(reach.get("tracer_init_mgL", "0")),
            )
        )
    reach_a, reach_b = reaches
    return reach_a, reach_b
