# Monolithic legacy script mixing I/O, globals, and computations.
# HINTS: globals, inconsistent naming, hard-coded paths, mixed responsibilities.

from __future__ import annotations


import csv
from typing import Any, Dict, List

from deltares_model.utils import read_csv_as_dicts
from deltares_model.forcing import initialize_forcing
from deltares_model.reach import initialize_reaches


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


def run_all(csv_forcing_path: str, csv_reaches_path: str) -> List[Dict[str, Any]]:
    """Runs the water balance model for all time steps of the forcing.

    Parameters
    ----------
    csv_forcing_path
        Path to the forcing CSV file.
    csv_reaches_path
        Path to the reaches CSV file.

    Returns
    -------
        State dictionary with results and last_q.
    """
    forcing_data = read_csv_as_dicts(csv_forcing_path)
    reach_data = read_csv_as_dicts(csv_reaches_path)

    forcings = initialize_forcing(forcing_data)
    reach_a, reach_b = initialize_reaches(reach_data)

    results: List[Dict[str, Any]] = []
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

    return results


def write_output_csv(path: str, results: List[Dict[str, Any]]) -> None:
    """Writes the output to a CSV file.

    Parameters
    ----------
    path
        The file path to write the CSV to.
    results
        The results dictionary containing the data to write.
    """
    fieldnames = ["date", "reach", "q_m3s", "c_mgL"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in results:
            w.writerow(r)


def calculate_waterbalance(
    path_reaches: str, path_forcing: str, path_output: str
) -> None:
    """Main function to run the water model and write output.

    Parameters
    ----------
    path_reaches : str
        Path to the reaches CSV file.
    path_forcing : str
        Path to the forcing CSV file.
    path_output : str
        Path to the output CSV file.
    """
    results = run_all(path_reaches, path_forcing)
    write_output_csv(path_output, results)
    print(f"Wrote {len(results)} rows to {path_output}")
