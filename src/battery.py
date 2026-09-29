#!/usr/bin/env python3

import sys
from pathlib import Path

pijuice_source = Path.home() / "PiJuice" / "Software" / "Source"
sys.path.insert(0, str(pijuice_source))

from pijuice import PiJuice

pj = PiJuice(1, 0x14)

charge = pj.status.GetChargeLevel()
status = pj.status.GetStatus()
voltage = pj.status.GetBatteryVoltage()
temperature = pj.status.GetBatteryTemperature()

results = [charge, status, voltage, temperature]

if any(r["error"] != "NO_ERROR" for r in results):
    print("ERROR: Unable to read PiJuice")
    for r in results:
        if r["error"] != "NO_ERROR":
            print(r)
    sys.exit(1)


s = status["data"]

print("PiJuice Battery")
print("----------------")
print(f"Charge      : {charge['data']}%")
print(f"Battery     : {s['battery']}")
print(f"Power input : {s['powerInput']}")
print(f"5V IO       : {s['powerInput5vIo']}")
print(f"Voltage     : {voltage['data'] / 1000:.3f} V")
print(f"Temperature : {temperature['data']}°C")
print(f"Fault       : {s['isFault']}")

