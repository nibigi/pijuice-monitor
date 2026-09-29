# PiJuice Monitor

A Raspberry Pi power and battery monitoring project using the PiJuice HAT.

Currently developed and tested on:

- Raspberry Pi 3B+
- Debian 13 (Trixie)
- Python 3.13
- PiJuice HAT
- I2C bus 1 / address 0x14

## Current Features

- Battery charge percentage
- Charging / discharging status
- Power input status
- Battery voltage
- Battery temperature
- PiJuice fault status

## Usage

Run:

```bash
python3 src/battery.py

## Example output

```text
PiJuice Battery
---------------
Charge      : 35%
Battery     : CHARGING_FROM_IN
Power input : PRESENT
5V IO       : NOT_PRESENT
Voltage     : 4.187 V
Temperature : 23°C
Fault       : False
```
