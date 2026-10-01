import csv
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path.home() / "PiJuice/Software/Source"))

from pijuice import PiJuice


INTERVAL_SECONDS = 5
ANOMALY_TEMPERATURE = 60


def read_value(result, name):
    if result["error"] != "NO_ERROR":
        raise RuntimeError(f"Unable to read {name}: {result['error']}")
    return result["data"]


def main():
    pj = PiJuice(1, 0x14)

    log_dir = Path(__file__).resolve().parents[1] / "logs"
    log_dir.mkdir(exist_ok=True)

    filename = log_dir / f"temperature_{datetime.now():%Y-%m-%d_%H-%M-%S}.csv"

    print("PiJuice Temperature Diagnostics")
    print("--------------------------------")
    print(f"Interval : {INTERVAL_SECONDS} seconds")
    print(f"Log file : {filename}")
    print("Press Ctrl+C to stop.")
    print()

    with filename.open("w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "temperature_c",
            "charge_percent",
            "voltage_v",
            "battery_state",
            "power_input",
            "fault",
            "temperature_status",
        ])

        try:
            while True:
                timestamp = datetime.now().isoformat(timespec="seconds")

                temperature = read_value(
                    pj.status.GetBatteryTemperature(),
                    "temperature",
                )

                charge = read_value(
                    pj.status.GetChargeLevel(),
                    "charge level",
                )

                voltage_mv = read_value(
                    pj.status.GetBatteryVoltage(),
                    "battery voltage",
                )

                status = read_value(
                    pj.status.GetStatus(),
                    "status",
                )

                fault = read_value(
                    pj.status.GetFaultStatus(),
                    "fault status",
                )

                temperature_status = (
                    "ANOMALY"
                    if temperature >= ANOMALY_TEMPERATURE
                    else "NORMAL"
                )

                writer.writerow([
                    timestamp,
                    temperature,
                    charge,
                    voltage_mv / 1000,
                    status["battery"],
                    status["powerInput"],
                    bool(fault),
                    temperature_status,
                ])

                file.flush()

                print(
                    f"{timestamp} | "
                    f"{temperature:3d}°C | "
                    f"{charge:3d}% | "
                    f"{voltage_mv / 1000:.3f}V | "
                    f"{status['battery']:<18} | "
                    f"{temperature_status}"
                )

                time.sleep(INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print()
            print("Logging stopped.")
            print(f"Saved: {filename}")


if __name__ == "__main__":
    main()
