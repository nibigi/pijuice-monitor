# PiJuice Monitor

A Raspberry Pi power and battery monitoring project using the PiJuice HAT.

The long-term goal is to build an autonomous Raspberry Pi power management
system capable of running from solar power, safely shutting down when the
battery is low, automatically restarting after sufficient recharge, and
reporting status and historical data to a web dashboard.

Currently developed and tested on:

- Raspberry Pi 3B+
- Debian 13 (Trixie)
- Python 3.13
- PiJuice HAT
- I2C bus 1 / address 0x14
- PiJuice firmware 1.5
- PiJuice battery profile BP7X_1820

## Current Features

- Battery charge percentage
- Charging / discharging status
- External power input detection
- Battery voltage
- Battery temperature
- PiJuice fault status
- Shared PiJuice sensor reader
- Battery temperature anomaly flagging
- Low-battery detection
- Low-battery confirmation before shutdown
- Safe-shutdown dry-run workflow
- Automated low-battery safety tests
- Low-battery simulation mode
- PiJuice delayed hardware power-off
- Persistent wake-up-on-charge configuration
- Historical battery data logging
- 60-second CSV data collection
- Historical logger managed by systemd
- Automatic historical logger startup after reboot
- Local web dashboard on port 8080
- Live PiJuice status API (`/api/status`)
- Historical data API (`/api/history`)
- Live dashboard status updates every 5 seconds without full-page reload
- Battery history SVG chart

## Installation

### 1. Enable I2C

Make sure I2C is enabled on the Raspberry Pi.

The PiJuice should normally appear on I2C bus 1 at address `0x14`.

Check with:

```bash
sudo i2cdetect -y 1
```

Expected PiJuice address:

```text
14
```

### 2. Install the PiJuice software

Clone the official PiJuice repository:

```bash
cd ~
git clone https://github.com/PiSupply/PiJuice.git
```

The Python PiJuice library used by this project is located under:

```text
~/PiJuice/Software/Source
```

### 3. Clone PiJuice Monitor

```bash
cd ~
git clone https://github.com/nibigi/pijuice-monitor.git
cd pijuice-monitor
```

### 4. Test communication with PiJuice

```bash
python3 -c "import sys; sys.path.insert(0, '/home/'\"$USER\"'/PiJuice/Software/Source'); from pijuice import PiJuice; p=PiJuice(1,0x14); print(p.status.GetChargeLevel())"
```

A successful response should contain:

```text
'error': 'NO_ERROR'
```

## Usage

### Battery status

Run:

```bash
python3 src/battery.py
```

Example output:

```text
PiJuice Battery
---------------

Charge      : 79%
Battery     : CHARGING_FROM_IN
Power input : PRESENT
5V IO       : NOT_PRESENT
Voltage     : 3.987 V
Temperature : 43°C
Temp status : NORMAL
Fault       : False
```

The battery status command uses the shared PiJuice reader in
`src/pijuice_reader.py`.

### Low-battery monitor

Run:

```bash
python3 src/low_battery_monitor.py
```

The current low-battery threshold is:

```text
20%
```

A shutdown candidate requires:

```text
Battery <= 20%
AND
External power = NOT_PRESENT
```

The condition is then confirmed three times, with 60 seconds between checks,
before a shutdown is considered confirmed.

### Simulation

The complete low-battery workflow can be tested without waiting for the
battery to discharge:

```bash
python3 src/low_battery_monitor.py --simulate-low
```

Example:

```text
Battery level : 15%
Battery state : NORMAL
Power input   : NOT_PRESENT
Threshold     : 20%
Battery is low and external power is not present.
Action        : SHUTDOWN CANDIDATE

Confirming low battery for 2 minutes...
Low battery confirmed.
Action        : SHUTDOWN CONFIRMED

Shutdown      : DRY RUN
Would schedule PiJuice power-off in 60 seconds and halt Linux.
```

The simulation currently uses dry-run mode and does not shut down the
Raspberry Pi.

## Historical Data Logging

PiJuice Monitor can record battery and power information to a CSV file every
60 seconds.

Run manually with:

```bash
python3 src/history_logger.py
```

Historical data is stored in:

```text
data/pijuice_history.csv
```

The CSV contains:

```text
timestamp
charge
battery
power_input
io_5v
voltage
temperature
temperature_status
fault
```

Example record:

```text
2026-10-01T20:27:41+01:00,83,CHARGING_FROM_IN,PRESENT,NOT_PRESENT,4.004,41,NORMAL,False
```

Runtime CSV files under `data/` and diagnostic CSV files under `logs/` are
excluded from Git.

### Historical logger systemd service

A systemd service is included at:

```text
systemd/pijuice-history.service
```

The historical logger has been tested running continuously in the background
and automatically starting again after a Raspberry Pi reboot.

Check the service:

```bash
sudo systemctl status pijuice-history.service
```

Start it:

```bash
sudo systemctl start pijuice-history.service
```

Stop it:

```bash
sudo systemctl stop pijuice-history.service
```

Enable automatic startup:

```bash
sudo systemctl enable pijuice-history.service
```

View recent historical records:

```bash
tail data/pijuice_history.csv
```

The current service file was tested with the project installed at:

```text
/home/<username>/pijuice-monitor
```

The paths in the service file must be adjusted if the project is installed
under a different user or directory.

## Web Dashboard

PiJuice Monitor includes a lightweight local web dashboard implemented
using the Python standard library.

Start the dashboard manually:

```bash
python3 src/web_dashboard.py
```

The dashboard listens on port 8080.

On the Raspberry Pi:
http://localhost:8080

From another device on the same local network:
http://raspberry-pi-hostname.local:8080

The dashboard currently displays:
- Battery charge percentage
- Charging / discharging state
- External power status
- Battery voltage
- Battery temperature
- Temperature NORMAL / ANOMALY status
- PiJuice fault status
- Battery history chart

### Live status API

Current PiJuice status is available from:
/api/status

For example:
curl http://localhost:8080/api/status

The web dashboard fetches this endpoint every 5 seconds and updates the status cards using JavaScript without reloading the entire page.

### Historical data API

Historical records are available from:
/api/history

For example:
curl http://localhost:8080/api/history

The API currently returns up to 120 recent records from data/pijuice_history.csv.
Historical data is collected independently by pijuice-history.service every 60 seconds.
The web dashboard itself is currently started manually and is not yet managed by systemd.

## Power Management

### Hardware power-off

PiJuice supports delayed hardware power-off using:

```python
p.power.SetPowerOff(60)
```

The 60-second delay allows Linux enough time to perform a safe shutdown before
PiJuice removes 5V power from the Raspberry Pi.

A controlled hardware test has been successfully completed:

```text
SetPowerOff(60)
        |
     sudo halt
        |
SSH disconnected after approximately 5 seconds
        |
Raspberry Pi power LED turned off
        |
PiJuice successfully removed 5V power
```

### Wake-up on charge

PiJuice is currently configured to wake the Raspberry Pi when the battery
reaches:

```text
40%
```

The setting is stored as non-volatile configuration:

```python
p.power.SetWakeUpOnCharge(40, True)
```

Current intended power-management thresholds:

```text
Shutdown threshold : 20%
Wake-up threshold  : 40%
```

The gap between the shutdown and wake-up levels is intended to prevent repeated
boot/shutdown cycles when using an intermittent power source such as solar.

Automatic wake-up after recharge still needs to be tested end-to-end.

## Temperature Diagnostics

A diagnostic logger is available for investigating the intermittent PiJuice
battery temperature readings.

Run:

```bash
python3 src/temperature_diagnostics.py
```

The diagnostic tool records readings every 5 seconds until stopped with
`Ctrl+C`.

Diagnostic CSV files are written under:

```text
logs/
```

These files are excluded from Git.

## Tests

Run the low-battery safety tests with:

```bash
python3 tests/test_low_battery.py
```

Expected result:

```text
All low-battery tests passed.
```

Check Python syntax with:

```bash
python3 -m py_compile src/low_battery_monitor.py
```

## Known Issues

### Intermittent battery temperature readings

The PiJuice battery temperature reading is currently unstable.

During testing, the reported temperature repeatedly jumped between plausible
values around 41–43°C and anomalous values around 80–90°C within only a few
seconds.

Direct reads from the PiJuice battery temperature register (`0x47`) confirmed
that these values are being returned by the PiJuice itself rather than being
introduced by `battery.py`.

Example observed readings:

```text
43°C
85°C
90°C
85°C
85°C
43°C
90°C
43°C
85°C
43°C
90°C
```

Longer diagnostic testing also produced readings such as 76°C and 80°C.

Current battery configuration:

```text
Firmware          : 1.5
Battery profile   : BP7X_1820
Profile status    : VALID
Capacity          : 1820 mAh
NTC resistance    : 10000 ohms
NTC B value       : 3380
Warm threshold    : 45°C
Hot threshold     : 59°C
```

The cause is still under investigation.

The diagnostic results show abrupt transitions between the lower and higher
temperature ranges. For example, readings can change from approximately 43°C
to 80–90°C and back again within only a few seconds. This behaviour is not
consistent with a real battery physically changing temperature at that rate.

PiJuice Monitor currently flags readings of 60°C or above as:

```text
ANOMALY
```

and lower readings as:

```text
NORMAL
```

This threshold is a diagnostic flag only. It does **not** mean that every
reading below 60°C has been proven accurate, or that every reading at or above
60°C is necessarily false.

For safety, battery temperature is currently treated as monitoring information
only and is **not used as an automatic shutdown trigger**.

## Project Structure

```text
pijuice-monitor/
├── README.md
├── data/
├── logs/
├── src/
│   ├── battery.py
│   ├── history_logger.py
│   ├── low_battery_monitor.py
│   ├── pijuice_reader.py
│   └── temperature_diagnostics.py
├── systemd/
│   └── pijuice-history.service
└── tests/
    └── test_low_battery.py
```

The `data/` and `logs/` directories contain runtime data and are not intended
to be committed to Git.

## Roadmap

- [x] PiJuice battery monitoring
- [x] Low-battery detection
- [x] External power detection
- [x] Low-battery confirmation (3 checks, 60 seconds apart)
- [x] Low-battery safety tests
- [x] Safe-shutdown dry-run workflow
- [x] Low-battery simulation mode
- [x] PiJuice hardware power-off test
- [x] Configure persistent wake-up on charge at 40%
- [x] Shared PiJuice sensor reader
- [x] Historical data logging
- [x] Historical logger systemd service
- [x] Historical logger automatic startup after reboot
- [ ] Integrate production low-battery safe shutdown
- [ ] Verify automatic restart after sufficient recharge
- [ ] Investigate intermittent battery temperature readings
- [ ] Run production low-battery monitor automatically as a system service
- [ ] System / CPU monitoring
- [ ] Solar power integration
- [x] Local web dashboard
- [x] Battery history chart
- [x] Historical data API (`/api/history`)
- [x] Live status API (`/api/status`)
- [x] Live dashboard updates without full-page reload
- [ ] Voltage history chart
- [ ] Temperature history chart
- [ ] Run web dashboard automatically as a system service
- [ ] Cloud data upload
- [ ] MQTT
- [ ] iPhone integration
