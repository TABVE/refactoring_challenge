from __future__ import annotations

# Entry point to run the legacy model and write results.
# Intentionally minimal and unclear (smell).

import argparse

from deltares_model.water_model import calculate_waterbalance


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate a daily water balance and a conservative tracer concentration across two linked river reaches."
    )
    parser.add_argument(
        "--forcing", help="Path to the forcing CSV file", default="data/forcing.csv"
    )
    parser.add_argument(
        "--reaches", help="Path to the reaches CSV file", default="data/reaches.csv"
    )
    parser.add_argument(
        "--out", help="Path to the output CSV file", default="results.csv"
    )
    args = parser.parse_args()

    calculate_waterbalance(args.forcing, args.reaches, args.out)
