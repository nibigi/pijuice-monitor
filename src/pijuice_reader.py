#!/usr/bin/env python3

import sys
from pathlib import Path

pijuice_source = Path.home() / "PiJuice" / "Software" / "Source"
sys.path.insert(0, str(pijuice_source))

from pijuice import PiJuice


# Diagnostics on 2026-10-01 showed two distinct clusters:
# 41-43°C and 80-90°C, with no readings between 44-79°C.
#
# For now, >= 60°C is therefore flagged as anomalous rather than
# interpreted as a confirmed physical battery temperature.
TEMPERATURE_ANOMALY_THRESHOLD = 60


def read_value(result, name):
    if result["error"] != "NO_ERROR":
        raise RuntimeError(
            f"Unable to read {name}: {result['error']}"
        )

    return result["data"]


def read_snapshot(pj=None):
    if pj is None:
        pj = PiJuice(1, 0x14)

    charge = read_value(
        pj.status.GetChargeLevel(),
        "charge level",
    )

    status = read_value(
        pj.status.GetStatus(),
        "status",
    )

    voltage_mv = read_value(
        pj.status.GetBatteryVoltage(),
        "battery voltage",
    )

    temperature = read_value(
        pj.status.GetBatteryTemperature(),
        "battery temperature",
    )

    temperature_status = (
        "ANOMALY"
        if temperature >= TEMPERATURE_ANOMALY_THRESHOLD
        else "NORMAL"
    )

    return {
        "charge": charge,
        "battery": status["battery"],
        "power_input": status["powerInput"],
        "io_5v": status["powerInput5vIo"],
        "voltage": voltage_mv / 1000,
        "temperature": temperature,
        "temperature_status": temperature_status,
        "fault": status["isFault"],
    }
