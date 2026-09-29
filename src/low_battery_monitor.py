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


def main():
    pj = PiJuice(1, 0x14)

    charge = pj.status.GetChargeLevel()
    status = pj.status.GetStatus()

    if charge["error"] != "NO_ERROR" or status["error"] != "NO_ERROR":
        print("ERROR: Unable to read PiJuice")
        sys.exit(1)

    level = charge["data"]
    battery_status = status["data"]["battery"]
    power_input = status["data"]["powerInput"]

    action, message = decide_action(level, power_input)

    print(f"Battery level : {level}%")
    print(f"Battery state : {battery_status}")
    print(f"Power input   : {power_input}")
    print(f"Threshold     : {LOW_BATTERY_THRESHOLD}%")
    print(message)
    print(f"Action        : {action}")


if __name__ == "__main__":
    main()
