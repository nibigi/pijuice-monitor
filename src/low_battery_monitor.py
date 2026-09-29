#!/usr/bin/env python3

import sys
from pathlib import Path

pijuice_source = Path.home() / "PiJuice" / "Software" / "Source"
sys.path.insert(0, str(pijuice_source))

from pijuice import PiJuice

LOW_BATTERY_THRESHOLD = 20

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

def main():
    pj = PiJuice(1, 0x14)

    def read_status():
        charge = pj.status.GetChargeLevel()
        status = pj.status.GetStatus()

        if charge["error"] != "NO_ERROR" or status["error"] != "NO_ERROR":
            raise RuntimeError("Unable to read PiJuice")

        return charge["data"], status["data"]

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
            new_level, new_status = read_status()
            return new_level, new_status["powerInput"]

        confirmed = confirm_low_battery(confirmation_read)

        if confirmed:
            print("Low battery confirmed.")
            print("Action        : SHUTDOWN CONFIRMED")
        else:
            print("Shutdown cancelled.")
            print("Action        : KEEP RUNNING")


if __name__ == "__main__":
    main()
