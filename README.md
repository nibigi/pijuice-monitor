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
- Low-battery detection
- Low-battery confirmation before shutdown
- Safe-shutdown dry-run workflow
- Automated low-battery safety tests
- Low-battery simulation mode
- PiJuice delayed hardware power-off
- Persistent wake-up-on-charge configuration

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

Charge      : 35%
Battery     : CHARGING_FROM_IN
Power input : PRESENT
5V IO       : NOT_PRESENT
Voltage     : 4.187 V
Temperature : 23°C
Fault       : False
```

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
values around 37–44°C and implausible values of 80–90°C within only a few
seconds.

Direct reads from the PiJuice battery temperature register (`0x47`) confirmed
that these values are being returned by the PiJuice itself rather than being
introduced by `battery.py`.

Example observed readings:

```text
40°C
41°C
40°C
85°C
85°C
40°C
40°C
90°C
85°C
85°C
41°C
```

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

For safety, battery temperature is currently treated as monitoring information
only and is **not used as an automatic shutdown trigger**.

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
- [ ] Integrate production low-battery safe shutdown
- [ ] Verify automatic restart after sufficient recharge
- [ ] Investigate intermittent battery temperature readings
- [ ] Run monitor automatically as a system service
- [ ] System / CPU monitoring
- [ ] Solar power integration
- [ ] Historical data logging
- [ ] Web dashboard
- [ ] Cloud data upload
- [ ] MQTT
- [ ] iPhone integration
