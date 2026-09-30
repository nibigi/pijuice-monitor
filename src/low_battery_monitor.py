#!/usr/bin/env python3

import sys
from pathlib import Path

pijuice_source = Path.home() / "PiJuice" / "Software" / "Source"
sys.path.insert(0, str(pijuice_source))

from pijuice import PiJuice

LOW_BATTERY_THRESHOLD = 20
POWER_OFF_DELAY = 60
WAKE_UP_CHARGE_LEVEL = 40
DRY_RUN = True

def decide_action(level, power_input):
    if level <= LOW_BATTERY_THRESHOLD:
        if power_input == "PRESENT":
            return "KEEP RUNNING", "Battery is low, but external power is present."

        return (
            "SHUTDOWN CANDIDATE",
            "Battery is low and external power is not present.",
        )

    return "KEEP RUNNING", "Battery level is OK."

def confirm_low_battery(read_status, checks=3, delay=60, sleep_fn=None):
    if sleep_fn is None:
        import time
        sleep_fn = time.sleep

    for check in range(checks):
        level, power_input = read_status()
        action, _ = decide_action(level, power_input)

        if action != "SHUTDOWN CANDIDATE":
            return False

        if check < checks - 1:
            sleep_fn(delay)

    return True

def schedule_safe_shutdown(pj, dry_run=True):
    if dry_run:
        return (
            "DRY RUN",
            f"Would schedule PiJuice power-off in {POWER_OFF_DELAY} seconds "
            "and halt Linux.",
        )

    result = pj.power.SetPowerOff(POWER_OFF_DELAY)

    if result["error"] != "NO_ERROR":
        return "ERROR", "Unable to schedule PiJuice power-off."

    return (
        "SHUTDOWN SCHEDULED",
        f"PiJuice power-off scheduled in {POWER_OFF_DELAY} seconds.",
    )


def main():
    simulate_low = "--simulate-low" in sys.argv

    pj = PiJuice(1, 0x14)

    def read_status():
        charge = pj.status.GetChargeLevel()
        status = pj.status.GetStatus()

        if charge["error"] != "NO_ERROR" or status["error"] != "NO_ERROR":
            raise RuntimeError("Unable to read PiJuice")

        return charge["data"], status["data"]

    if simulate_low:
        level = 15
        status_data = {
            "battery": "NORMAL",
            "powerInput": "NOT_PRESENT",
        }
    else:
        try:
            level, status_data = read_status()
        except RuntimeError as error:
            print(f"ERROR: {error}")
            sys.exit(1)

    battery_status = status_data["battery"]
    power_input = status_data["powerInput"]

    action, message = decide_action(level, power_input)

    print(f"Battery level : {level}%")
    print(f"Battery state : {battery_status}")
    print(f"Power input   : {power_input}")
    print(f"Threshold     : {LOW_BATTERY_THRESHOLD}%")
    print(message)
    print(f"Action        : {action}")

    if action == "SHUTDOWN CANDIDATE":
        print()
        print("Confirming low battery for 2 minutes...")

        def confirmation_read():
            if simulate_low:
                return 15, "NOT_PRESENT"

            new_level, new_status = read_status()
            return new_level, new_status["powerInput"]

        if simulate_low:
            confirmed = confirm_low_battery(
                confirmation_read,
                sleep_fn=lambda seconds: None,
            )
        else:
            confirmed = confirm_low_battery(confirmation_read)

        if confirmed:
            print("Low battery confirmed.")
            print("Action        : SHUTDOWN CONFIRMED")
            print()

            shutdown_status, shutdown_message = schedule_safe_shutdown(
                pj,
                dry_run=DRY_RUN,
            )

            print(f"Shutdown      : {shutdown_status}")
            print(shutdown_message)
        else:
            print("Shutdown cancelled.")
            print("Action        : KEEP RUNNING")


if __name__ == "__main__":
    main()
