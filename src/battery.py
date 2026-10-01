#!/usr/bin/env python3

import sys

from pijuice_reader import read_snapshot


def main():
    try:
        reading = read_snapshot()
    except RuntimeError as error:
        print(f"ERROR: {error}")
        sys.exit(1)

    print("PiJuice Battery")
    print("----------------")
    print(f"Charge      : {reading['charge']}%")
    print(f"Battery     : {reading['battery']}")
    print(f"Power input : {reading['power_input']}")
    print(f"5V IO       : {reading['io_5v']}")
    print(f"Voltage     : {reading['voltage']:.3f} V")
    print(f"Temperature : {reading['temperature']}°C")
    print(f"Temp status : {reading['temperature_status']}")
    print(f"Fault       : {reading['fault']}")


if __name__ == "__main__":
    main()

