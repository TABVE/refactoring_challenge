# Monolithic legacy script mixing I/O, globals, and computations.
# HINTS: globals, inconsistent naming, hard-coded paths, mixed responsibilities.

from __future__ import annotations


import csv
import math
from typing import Any, Dict, List

from legacy_code.config import CONFIG
from legacy_code.utils import parse_date, read_csv_as_dicts
from legacy_code.forcing import initialize_forcing
from legacy_code.reach import initialize_reaches


def mm_day_to_m3s(mm_per_day: float, area_km2: float) -> float:
    """Converts mm/day over area_km2 to m^3/s.
    Formula: (mm/1000) * (area_km2*1e6) / 86400

    Parameters
    ----------
    mm_per_day : float
        Depth in mm/day.
    area_km2 : float
        Area in km^2.

    Returns
    -------
    float
        Flow in m^3/s, nan if area_km2 is zero.

    Raises
    ------
    ValueError
        If area_km2 is negative.
    """
    if area_km2 == 0:
        return float("nan")
    elif area_km2 < 0:
        raise ValueError("area_km2 cannot be negative")
    try:
        return (mm_per_day / 1e3) * (area_km2 * 1e6) / 86400
    except Exception:
        return 0.0


def mix_concentration(q1: float, c1: float, q2: float, c2: float) -> float:
    """Calculates mixed concentration from two flows and concentrations.
    Formula: (q1*c1 + q2*c2)/(q1+q2) when q1+q2>0.

    Parameters
    ----------
    q1 : float
        Flow 1 in m^3/s.
    c1 : float
        Concentration 1 in mg/L.
    q2 : float
        Flow 2 in m^3/s.
    c2 : float
        Concentration 2 in mg/L.

    Returns
    -------
    float
        Mixed concentration in mg/L, nan if total flow is negative.

    Raises
    ------
    ValueError
        If total flow (q1 + q2) is negative.
    """
    try:
        if q1 + q2 == 0:
            return 0
        elif q1 + q2 < 0:
            return float("nan")
        else:
            return (q1 * c1 + q2 * c2) / (q1 + q2)
    except Exception:
        return float("nan")


def run_all() -> Dict[str, Any]:
    state: Dict[str, Any] = {
        "last_q": 0.0,
        "rows": [],
    }
    fpath = CONFIG.get("paths", {}).get("forcing") or "data/forcing.csv"
    rpath = CONFIG.get("paths", {}).get("reaches") or "data/reaches.csv"

    forcing = read_csv_as_dicts(fpath)
    reaches = read_csv_as_dicts(rpath)
    if len(reaches) < 2:
        raise RuntimeError("need at least 2 reaches A and B")

    results: List[Dict[str, Any]] = []

    forcings = initialize_forcing(forcing)
    reach_a, reach_b = initialize_reaches(reaches)

    for forcing in forcings:
        date = forcing.date

        precipitation = forcing.precipitation
        evaporation = forcing.evapotranspiration
        upstream_concentration = forcing.upstream_tracer_concentration

        reach_a.run_off = max(precipitation - evaporation, 0.0)
        reach_b.run_off = max(precipitation - evaporation, 0.0)

        reach_a.local_flow_rate = mm_day_to_m3s(reach_a.run_off, reach_a.area)
        reach_b.local_flow_rate = mm_day_to_m3s(reach_b.run_off, reach_b.area)

        # Reach A total discharge (no routing)
        reach_a.last_flow_rate = reach_a.local_flow_rate

        # Mix tracer in A: upstream boundary and local input
        reach_a.last_concentration = mix_concentration(
            q1=1.0,  # TODO: discuss with collegues, why 1.0 here?
            c1=upstream_concentration,
            q2=reach_a.local_flow_rate,
            c2=reach_a.last_concentration,
        )

        results.append(
            {
                "date": date.isoformat(),
                "reach": reach_a.id,
                "q_m3s": reach_a.last_flow_rate,
                "c_mgL": reach_a.last_concentration,
            }
        )

        # Reach B receives Q from A and its own local input
        reach_b.last_flow_rate = reach_b.local_flow_rate + reach_a.last_flow_rate

        reach_b.last_concentration = mix_concentration(
            q1=reach_a.last_flow_rate,
            c1=reach_a.last_concentration,
            q2=reach_b.local_flow_rate,
            c2=reach_b.last_concentration,
        )

        results.append(
            {
                "date": date.isoformat(),
                "reach": reach_b.id,
                "q_m3s": reach_b.last_flow_rate,
                "c_mgL": reach_b.last_concentration,
            }
        )

    state["rows"] = results
    return state


def write_output_csv(path: str, state) -> None:
    """Writes the output to a CSV file.

    Parameters
    ----------
    path
        The file path to write the CSV to.
    """
    rows = state.get("rows") or []
    fieldnames = ["date", "reach", "q_m3s", "c_mgL"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> None:
    """Main function to run the water model and write output."""
    # Hard-coded default path — smell
    path_out = CONFIG.get("paths", {}).get("output", "legacy_results.csv")
    state = run_all()
    write_output_csv(path_out, state)
    print(f"Wrote {len(state["rows"])} rows to {path_out}")
