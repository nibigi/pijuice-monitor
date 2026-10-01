#!/usr/bin/env python3

import csv
import sys
import time
from datetime import datetime
from pathlib import Path

from pijuice_reader import read_snapshot


INTERVAL_SECONDS = 60

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CSV_FILE = DATA_DIR / "pijuice_history.csv"

FIELDNAMES = [
    "timestamp",
    "charge",
    "battery",
    "power_input",
    "io_5v",
    "voltage",
    "temperature",
    "temperature_status",
    "fault",
]


def ensure_csv():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not CSV_FILE.exists():
        with CSV_FILE.open("w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def write_record(record):
    with CSV_FILE.open("a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(record)


def main():
    ensure_csv()

    print("PiJuice Historical Logger")
    print("-------------------------")
    print(f"Interval : {INTERVAL_SECONDS} seconds")
    print(f"Output   : {CSV_FILE}")
    print()
    print("Press Ctrl+C to stop.")
    print()

    try:
        while True:
            try:
                reading = read_snapshot()

                record = {
                    "timestamp": datetime.now()
                    .astimezone()
                    .isoformat(timespec="seconds"),
                    **reading,
                }

                write_record(record)

                print(
                    f"{record['timestamp']} | "
                    f"{record['charge']}% | "
                    f"{record['battery']} | "
                    f"{record['voltage']:.3f} V | "
                    f"{record['temperature']}°C | "
                    f"{record['temperature_status']}"
                )

            except RuntimeError as error:
                print(
                    f"{datetime.now().astimezone().isoformat(timespec='seconds')} "
                    f"| ERROR | {error}",
                    file=sys.stderr,
                )

            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nLogger stopped.")


if __name__ == "__main__":
    main()

