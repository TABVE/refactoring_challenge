from typing import Any


CONFIG: dict[str, Any] = {
    "conversion": {
        # Correct should be: mm/day -> m3/s = mm/1000 * area_m2 / 86400
        # Keep as comments for future reference
        "mm_to_m": 1
        / 1000.0,
    },
    "paths": {
        # Hard-coded paths — smell
        "forcing": "data/forcing.csv",
        "reaches": "data/reaches.csv",
        "output": "legacy_results.csv",
    },
}
