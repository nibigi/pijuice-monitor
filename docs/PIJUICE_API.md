# PiJuice Python Get/Set API reference
66 Get/Set entries in five classes. Click a function for its notes, return value and any earlier test result.

## PiJuice API Inventory

### PiJuiceInterface · 1 method

| Get | Set |
| --- | --- |
| [`GetAddress`](#pijuiceinterface-getaddress) | — |

### PiJuiceStatus · 19 methods

| Get | Set |
| --- | --- |
| [`GetStatus`](#pijuicestatus-getstatus) | — |
| [`GetChargeLevel`](#pijuicestatus-getchargelevel) | — |
| [`GetFaultStatus`](#pijuicestatus-getfaultstatus) | — |
| [`GetButtonEvents`](#pijuicestatus-getbuttonevents) | — |
| [`GetBatteryTemperature`](#pijuicestatus-getbatterytemperature) | — |
| [`GetBatteryVoltage`](#pijuicestatus-getbatteryvoltage) | — |
| [`GetBatteryCurrent`](#pijuicestatus-getbatterycurrent) | — |
| [`GetIoVoltage`](#pijuicestatus-getiovoltage) | — |
| [`GetIoCurrent`](#pijuicestatus-getiocurrent) | — |
| [`GetLedState`](#pijuicestatus-getledstate) | [`SetLedState`](#pijuicestatus-setledstate) |
| [`GetLedBlink`](#pijuicestatus-getledblink) | [`SetLedBlink`](#pijuicestatus-setledblink) |
| [`GetIoDigitalInput`](#pijuicestatus-getiodigitalinput) | — |
| [`GetIoDigitalOutput`](#pijuicestatus-getiodigitaloutput) | [`SetIoDigitalOutput`](#pijuicestatus-setiodigitaloutput) |
| [`GetIoAnalogInput`](#pijuicestatus-getioanaloginput) | — |
| [`GetIoPWM`](#pijuicestatus-getiopwm) | [`SetIoPWM`](#pijuicestatus-setiopwm) |

### PiJuiceRtcAlarm · 6 methods

| Get | Set |
| --- | --- |
| [`GetControlStatus`](#pijuicertcalarm-getcontrolstatus) | — |
| [`GetTime`](#pijuicertcalarm-gettime) | [`SetTime`](#pijuicertcalarm-settime) |
| [`GetAlarm`](#pijuicertcalarm-getalarm) | [`SetAlarm`](#pijuicertcalarm-setalarm) |
| — | [`SetWakeupEnabled`](#pijuicertcalarm-setwakeupenabled) |

### PiJuicePower · 8 methods

| Get | Set |
| --- | --- |
| [`GetPowerOff`](#pijuicepower-getpoweroff) | [`SetPowerOff`](#pijuicepower-setpoweroff) |
| [`GetWakeUpOnCharge`](#pijuicepower-getwakeuponcharge) | [`SetWakeUpOnCharge`](#pijuicepower-setwakeuponcharge) |
| [`GetWatchdog`](#pijuicepower-getwatchdog) | [`SetWatchdog`](#pijuicepower-setwatchdog) |
| [`GetSystemPowerSwitch`](#pijuicepower-getsystempowerswitch) | [`SetSystemPowerSwitch`](#pijuicepower-setsystempowerswitch) |

### PiJuiceConfig · 32 methods

| Get | Set |
| --- | --- |
| [`GetChargingConfig`](#pijuiceconfig-getchargingconfig) | [`SetChargingConfig`](#pijuiceconfig-setchargingconfig) |
| [`GetBatteryProfileStatus`](#pijuiceconfig-getbatteryprofilestatus) | [`SetBatteryProfile`](#pijuiceconfig-setbatteryprofile) |
| [`GetBatteryProfile`](#pijuiceconfig-getbatteryprofile) | [`SetCustomBatteryProfile`](#pijuiceconfig-setcustombatteryprofile) |
| [`GetBatteryExtProfile`](#pijuiceconfig-getbatteryextprofile) | [`SetCustomBatteryExtProfile`](#pijuiceconfig-setcustombatteryextprofile) |
| [`GetBatteryTempSenseConfig`](#pijuiceconfig-getbatterytempsenseconfig) | [`SetBatteryTempSenseConfig`](#pijuiceconfig-setbatterytempsenseconfig) |
| [`GetRsocEstimationConfig`](#pijuiceconfig-getrsocestimationconfig) | [`SetRsocEstimationConfig`](#pijuiceconfig-setrsocestimationconfig) |
| [`GetPowerInputsConfig`](#pijuiceconfig-getpowerinputsconfig) | [`SetPowerInputsConfig`](#pijuiceconfig-setpowerinputsconfig) |
| [`GetButtonConfiguration`](#pijuiceconfig-getbuttonconfiguration) | [`SetButtonConfiguration`](#pijuiceconfig-setbuttonconfiguration) |
| [`GetLedConfiguration`](#pijuiceconfig-getledconfiguration) | [`SetLedConfiguration`](#pijuiceconfig-setledconfiguration) |
| [`GetPowerRegulatorMode`](#pijuiceconfig-getpowerregulatormode) | [`SetPowerRegulatorMode`](#pijuiceconfig-setpowerregulatormode) |
| [`GetRunPinConfig`](#pijuiceconfig-getrunpinconfig) | [`SetRunPinConfig`](#pijuiceconfig-setrunpinconfig) |
| [`GetIoConfiguration`](#pijuiceconfig-getioconfiguration) | [`SetIoConfiguration`](#pijuiceconfig-setioconfiguration) |
| [`GetAddress`](#pijuiceconfig-getaddress) | [`SetAddress`](#pijuiceconfig-setaddress) |
| [`GetIdEepromWriteProtect`](#pijuiceconfig-getideepromwriteprotect) | [`SetIdEepromWriteProtect`](#pijuiceconfig-setideepromwriteprotect) |
| [`GetIdEepromAddress`](#pijuiceconfig-getideepromaddress) | [`SetIdEepromAddress`](#pijuiceconfig-setideepromaddress) |
| [`GetFirmwareVersion`](#pijuiceconfig-getfirmwareversion) | — |
| — | [`SetDefaultConfiguration`](#pijuiceconfig-setdefaultconfiguration) |

### Reference sections

[Scope and official references](#scope-and-evidence) · [Returns and errors](#return-and-error-conventions) · [Shared field schemas](#shared-field-schemas) · [Historical comparison](#comparison-with-historical-tests) · [Method details](#method-details) · [Interpretation limits](#interpretation-limits)

---

## Scope and evidence

This list has **66 Get/Set entries** in five classes (1 + 19 + 6 + 8 + 32). The original count was 63, but the full list adds up to 66. `GetAddress` appears in two classes. Other library functions are outside this list.



Checked against Pi Supply code revision `df8674691bd376170cfc4659d8f2e2fbebed29b3`, Python library **1.8**. The installed function names match, but the exact installed code revision is still unknown. Library and firmware versions can affect the results.

Official references:

- [Python library source](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py): authoritative here for Python return shapes, decoding and error branches. Each method below links to its own lines.
- [Manufacturer software documentation and I2C/Python API](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/README.md#i2c-command-api): units, feature meanings and examples; some examples predate the pinned implementation.
- [Manufacturer hardware documentation and battery profiles](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Hardware/README.md#battery-profiles): power connections and battery profile characteristics.

If an official example differs from this code, the difference is noted. Units or special values that could not be confirmed are left as unknown.

## Refresh the inventory safely

Run this read-only extraction on the Pi only when an inventory refresh is
needed; it parses source without importing PiJuice or touching I2C:

```bash
python3 - <<'PY'
import ast
from pathlib import Path
path = Path.home() / 'PiJuice/Software/Source/pijuice.py'
tree = ast.parse(path.read_text())
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        methods = [item.name for item in node.body
                   if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and item.name.startswith(('Get', 'Set'))]
        if methods:
            print(f'[{node.name}] ({len(methods)})')
            print(', '.join(methods))
PY
```

The extraction does not establish the upstream revision. Record that revision
separately if a future release needs version-specific API documentation.

## Return and error conventions

Most functions return a Python dictionary. These are the common formats:

- **R(data)**: `{'error': 'NO_ERROR', 'data': <described value>}` on success. When stated, `non_volatile` is an additional **outer** boolean key, not inside `data`.
- **W**: `{'error': 'NO_ERROR'}` on a completed write; no `data` and no read-back verification. This is not proof of the intended physical effect.
- **V**: same success shape as W, after `WriteDataVerify` writes and reads the bytes back. A mismatch returns `{'error': 'WRITE_FAILED'}`. Special verification behavior is stated per method.
- Transport failures return `{'error': 'COMMUNICATION_ERROR'}`; reads can return `{'error': 'DATA_CORRUPTED'}` for checksum mismatch. A verified write can encounter either read error as well as WRITE_FAILED. Usually failure dictionaries have no `data`; check `error` before accessing it.
- COMMUNICATION_ERROR covers caught bus failures, transfer timeout/busy thread and a short post-error backoff. DATA_CORRUPTED follows the source's retry of the checksum with the first byte's top bit set. These strings are library diagnostics, not a diagnosis of battery condition.
- Each "Errors mentioned in the code" list shows error strings present in that function, in addition to the common transport/verification errors. Some listed branches may not be reached; the function notes explain these cases. This is not a list of every possible Python exception. Malformed objects, reserved codes or uncaught conversions may raise Python exceptions instead of returning a dictionary. A method can quantise, mask or wrap an input without reporting an error.
- `PiJuiceInterface.GetAddress()` is the exception to the dictionary convention: it returns a cached integer directly.

Set functions change settings and can affect charging, power or wakeup. They were not run again for this update; these notes use official code and earlier test records.

## Shared field schemas

### BatteryProfile

`data` has all of: `capacity`, `chargeCurrent`, `terminationCurrent`, `regulationVoltage`, `cutoffVoltage`, `tempCold`, `tempCool`, `tempWarm`, `tempHot`, `ntcB`, `ntcResistance` (integers).

| Fields | Units and source behavior |
| --- | --- |
| capacity | mAh (manufacturer hardware profile examples). Decoder expands packed capacity; 0xFFFF becomes sentinel 0xFFFFFFFF. Physical meaning of that sentinel is not established here. |
| chargeCurrent, terminationCurrent | mA; source decoding: byte × 75 + 550; byte × 50 + 50 respectively. |
| regulationVoltage, cutoffVoltage | mV; byte × 20 + 3500; byte × 20 respectively. |
| tempCold, tempCool, tempWarm, tempHot | Signed temperature thresholds; manufacturer describes cold/hot suspension, cool reduced charge current, warm reduced regulation voltage. °C is the temperature convention in the manufacturer API; source uses signed bytes. |
| ntcB | Thermistor B constant, unsigned 16-bit. Reviewed Python/API prose does not explicitly label its unit; do not treat it as a temperature reading. |
| ntcResistance | Nominal thermistor resistance at 25°C, ohms (hardware specifies a 10 kΩ NTC; source exposes 10000 for that profile), decoded unsigned 16-bit × 10. |

Manufacturer operating ranges and a byte's representable range are different. Source-derived encoding ranges are not safe battery limits.

### ExtendedProfile

`chemistry`: LIPO / LIFEPO4 / UNKNOWN. `ocv10`, `ocv50`, `ocv90`: unsigned 16-bit integers. `r10`, `r50`, `r90`: floats, unsigned 16-bit / 100. The field names suggest open-circuit voltage and resistance at charge-level points, but the reviewed Python source and API prose do not establish the units or precise test conditions. They are **unverified** here; do not label them V/mV or Ω/mΩ without an additional manufacturer specification. Setter uses only LIPO/LIFEPO4.

### PowerInputs

`precedence`: USB_MICRO / 5V_GPIO; `gpio_in_enabled`, `no_battery_turn_on`: bool; `usb_micro_current_limit`: "1.5A" / "2.5A"; `usb_micro_dpm`: "4.20V", "4.28V", "4.36V", "4.44V", "4.52V", "4.60V", "4.68V", "4.76V". These are string settings, not numeric measured currents/voltages. DPM is the input voltage regulation threshold.

### IoConfiguration

Every returned object has `mode` and `pull`. mode: NOT_USED / ANALOG_IN / DIGITAL_IN / DIGITAL_OUT_PUSHPULL / DIGITAL_IO_OPEN_DRAIN / PWM_OUT_PUSHPULL / PWM_OUT_OPEN_DRAIN, or UNKNOWN. pull: NOPULL / PULLDOWN / PULLUP, or UNKNOWN.

- Digital output modes add `value` (integer decoded byte; not normalised to bool).
- PWM modes add `period` (integer µs, `(raw16+1)*2`) and `duty_cycle` (%, same floor-division behavior as GetIoPWM; 100% returns integer 100).
- Other modes, including NOT_USED/ANALOG_IN/UNKNOWN, add `wakeup` (NO_WAKEUP / FALLING_EDGE / RISING_EDGE / empty string for reserved code). This reflects the wrapper branch, not a promise of wakeup support in every mode.
- Setter needs `mode`, `pull` plus the applicable mode fields; for DIGITAL_IN it requires the wakeup key, with a false value treated as NO_WAKEUP. Documented PWM metadata range is 2–131072 µs. Pin designators are 1/2.

Button function names in source: NO_FUNC; HARD_FUNC_POWER_ON / HARD_FUNC_POWER_OFF / HARD_FUNC_RESET; SYS_FUNC_HALT / SYS_FUNC_HALT_POW_OFF / SYS_FUNC_SYS_OFF_HALT / SYS_FUNC_REBOOT; USER_EVENT and USER_FUNC1 through USER_FUNC15. Unknown decoded values may be UNKNOWN.


## Comparison with historical tests

The earlier setup used a PiJuice HAT and Raspberry Pi 3B+, on I2C bus 1/address 0x14. One firmware check returned 1.5, variant 0. The exact installed Python code revision is unknown, and the tests were not all taken under the same confirmed conditions. Official code links use the revision listed above.

Each function has a **Test result** note. "No test result recorded" means no result was found in the earlier notes, not that the function failed or was never tested. Official examples, function-name checks and simulations are kept separate from hardware results.

| Comparison area | Finding | Limit |
| --- | --- | --- |
| Raw API structures | Direct samples for status, charge, measurements, faults, profile, charging config, firmware and power settings agree with the documented source shapes. | Samples validate selected successful paths, not every branch or setter. |
| Voltage units | Raw battery/IO results are in mV; application battery voltage is divided by 1000 into V. | Different-time readings are not paired calibration measurements. |
| Battery temperature | Integer return structure agrees; abrupt 37°C/80–85°C changes and a 90°C sample were reported despite NO_ERROR. | Physical accuracy/root cause remains unresolved. ANOMALY is application policy, not a manufacturer API field. |
| Battery current sign | Positive and negative integers were observed; -537 mA appeared with CHARGING_FROM_IN. | Cannot infer a universal charging/discharging sign convention from these samples. |
| Wake on charge | 40% and non_volatile True were read back after the setter. | Automatic restart after recharge and full power-loss persistence were not established. |
| Power-off register | Getter returned [255], matching its list shape. | Meaning of 255 remains unverified against the reviewed specification. |
| Argument errors | Missing io_pin produced a Python TypeError. | No successful GetIoConfiguration result is available for comparison. |

## Method details

### PiJuiceInterface (1)

<a id="pijuiceinterface-getaddress"></a>

#### `GetAddress()`

Returns a plain integer: the address cached in this interface instance. No `data`/`error` envelope, no I2C read. This differs from `PiJuiceConfig.GetAddress(slave)`.

[Official code, lines 43–44](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L43-L44).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

### PiJuiceStatus (19)

<a id="pijuicestatus-getstatus"></a>

#### `GetStatus()`

Returns `data`: object with `isFault`, `isButton` (bool); `battery` = NORMAL / CHARGING_FROM_IN / CHARGING_FROM_5V_IO / NOT_PRESENT; `powerInput`, `powerInput5vIo` = NOT_PRESENT / BAD / WEAK / PRESENT. These refer to PiJuice micro-USB and GPIO 5 V inputs respectively. NORMAL means present and not charging. Flags indicate pending faults/button events, not their details.

[Official code, lines 165–180](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L165-L180).

**Test result:** Earlier output: `{'data': {'isFault': True, 'isButton': False, 'battery': 'CHARGING_FROM_IN', 'powerInput': 'WEAK', 'powerInput5vIo': 'NOT_PRESENT'}, 'error': 'NO_ERROR'}`. The fields and values match the official code; this does not confirm the electrical cause of WEAK.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getchargelevel"></a>

#### `GetChargeLevel()`

Returns `data`: integer battery charge percentage (manufacturer: 0–100%). The decoder returns the byte unchanged and does not enforce that range. A zero reading alone does not confirm battery absence; manufacturer notes absence detection is limited when powered by onboard micro-USB.

[Official code, lines 182–187](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L182-L187).

**Test result:** Earlier outputs include `{'data': 51, 'error': 'NO_ERROR'}` and data 66. The percentage and dictionary format match the official notes. The charge estimate was not checked against a separate measurement.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getfaultstatus"></a>

#### `GetFaultStatus()`

Returns `data`: dictionary containing only the active flags. It can be empty (`{}`). Present flags `button_power_off`, `forced_power_off`, `forced_sys_power_off`, `watchdog_reset`, `battery_profile_invalid` have value True. `charging_temperature_fault`, when present, is SUSPEND / COOL / WARM. Normal temperature and unset flags are omitted, not returned as False.

[Official code, lines 193–213](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L193-L213).

**Test result:** Earlier output: `{'data': {'forced_power_off': True}, 'error': 'NO_ERROR'}`. A later posted result after clearing that flag was `{'data': {}, 'error': 'NO_ERROR'}`. Both agree with the way the code leaves out inactive flags. A stored forced_power_off flag does not by itself prove a present overheating condition or identify its cause.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getbuttonevents"></a>

#### `GetButtonEvents()`

Returns `data`: object with SW1, SW2, SW3; each is NO_EVENT / PRESS / RELEASE / SINGLE_PRESS / DOUBLE_PRESS / LONG_PRESS1 / LONG_PRESS2, or UNKNOWN for an unknown code. Reading is distinct from acknowledging events; acknowledgement methods are outside this Get/Set inventory.

[Official code, lines 226–246](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L226-L246).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getbatterytemperature"></a>

#### `GetBatteryTemperature()`

Returns `data`: signed integer °C. Although two bytes are read, only the first byte is decoded as signed 8-bit. Sensor selection is controlled by battery temperature configuration; this is not necessarily a direct cell sensor reading.

[Official code, lines 258–267](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L258-L267).

**Test result:** Earlier output includes `{'data': 36, 'error': 'NO_ERROR'}` and data 90. One posted ten-read sequence was 80, 85, 80, 80, 80, 37, 80, 80, 85, 37, all NO_ERROR. Return type agrees with the °C API, but physical accuracy is unresolved: successful communication does not validate the sensor. The project flags readings >=60°C as ANOMALY; that is an application diagnostic threshold, not a manufacturer limit or proof that readings below it are physically valid.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getbatteryvoltage"></a>

#### `GetBatteryVoltage()`

Returns `data`: unsigned 16-bit integer battery voltage in mV, little-endian decoding.

[Official code, lines 269–275](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L269-L275).

**Test result:** Earlier outputs include `{'data': 3919, 'error': 'NO_ERROR'}` and data 4163. Shape agrees; manufacturer unit is mV, so these correspond to 3.919 V and 4.163 V. The supplied application reader explicitly divides this API value by 1000; application volt values must not be described as raw API output.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getbatterycurrent"></a>

#### `GetBatteryCurrent()`

Returns `data`: signed 16-bit integer battery current in mA. The reviewed API prose establishes the unit but does not confirm the battery-current sign convention; do not infer charging/discharging from sign here.

[Official code, lines 277–286](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L277-L286).

**Test result:** Earlier outputs include `{'data': -537, 'error': 'NO_ERROR'}`, data 34, and data 113. The code supports these positive and negative values; unit is mA in the official notes. The -537 sample appeared alongside CHARGING_FROM_IN. These uncontrolled samples do not establish a general battery-current sign convention or charging accuracy.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getiovoltage"></a>

#### `GetIoVoltage()`

Returns `data`: unsigned 16-bit integer GPIO 5 V rail voltage in mV. This is the power rail, distinct from the IO1/IO2 analog input.

[Official code, lines 288–294](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L288-L294).

**Test result:** Earlier outputs: `{'data': 4942, 'error': 'NO_ERROR'}` and data 5001. The number format matches the code; manufacturer mV unit gives 4.942 V and 5.001 V. No independent voltmeter result was supplied.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getiocurrent"></a>

#### `GetIoCurrent()`

Returns `data`: signed 16-bit integer GPIO rail current in mA. Manufacturer GUI documentation: positive flows PiJuice → Raspberry Pi; negative flows Raspberry Pi → PiJuice.

[Official code, lines 296–305](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L296-L305).

**Test result:** Earlier outputs: `{'data': 897, 'error': 'NO_ERROR'}` and data 987. The number format matches the code; unit is mA. Positive values are compatible with the documented PiJuice-to-Pi direction, but a controlled bidirectional sign test was not supplied.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-setledstate"></a>

#### `SetLedState(led, rgb)`

Returns `{'error': 'NO_ERROR'}` after writing. Sets `[r,g,b]` brightness bytes for D1 or D2 configured as USER_LED. Manufacturer range per component: 0–255. No returned RGB or read-back verification.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 308–314](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L308-L314).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getledstate"></a>

#### `GetLedState(led)`

Returns `data`: list `[r,g,b]`, three unsigned brightness bytes (0–255), for D1/D2; not a named RGB object.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 316–322](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L316-L322).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-setledblink"></a>

#### `SetLedBlink(led, count, rgb1, period1, rgb2, period2)`

Returns `{'error': 'NO_ERROR'}` after writing. D1/D2; count 1–254 for finite blinks, 255 indefinite in the official notes. RGB lists contain three brightness bytes. Periods are milliseconds, manufacturer range 10–2550; source encodes `period//10` masked to a byte and count masked to a byte, rather than validating those ranges.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 324–333](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L324-L333).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getledblink"></a>

#### `GetLedBlink(led)`

Returns `data`: object `count` (byte), `rgb1`, `rgb2` (three-byte lists), `period1`, `period2` (integer ms, byte × 10). Count 255 denotes indefinite blinking in the official notes. Meaning of count 0 is not confirmed here.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 335–355](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L335-L355).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getiodigitalinput"></a>

#### `GetIoDigitalInput(pin)`

Returns `data`: integer 0/1 for low/high on IO1/IO2 (`pin` 1/2). Source returns 1 only when the input byte equals 1; every other byte maps to 0. Pin must be configured appropriately.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 357–366](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L357-L366).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-setiodigitaloutput"></a>

#### `SetIoDigitalOutput(pin, value)`

Returns `{'error': 'NO_ERROR'}` after writing. IO1/IO2 (`pin` 1/2). Writes low for value == 0, high otherwise; no read-back or validation that value is exactly 0/1.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 368–373](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L368-L373).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getiodigitaloutput"></a>

#### `GetIoDigitalOutput(pin)`

Returns `data`: integer 0/1, current output setting on IO1/IO2. Decodes the second byte as 1 only if exactly 1, otherwise 0.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 375–384](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L375-L384).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getioanaloginput"></a>

#### `GetIoAnalogInput(pin)`

Returns `data`: unsigned 16-bit integer analog input voltage in mV. Status method accepts pin 1/2, but source `ioSupportedModes` only lists ANALOG_IN for IO1; acceptance of a pin argument does not prove hardware analog support.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 386–394](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L386-L394).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-setiopwm"></a>

#### `SetIoPWM(pin, dutyCycle)`

Returns `{'error': 'NO_ERROR'}` after writing. Sets IO1/IO2 duty cycle in %. Conversion failure → BAD_ARGUMENT; outside 0–100 → INVALID_DUTY_CYCLE. Below 100 the source uses `int(round(dc*65534//100))`; 100 encodes 65535. No waveform is returned.

Errors mentioned in the code: `BAD_ARGUMENT`, `INVALID_DUTY_CYCLE`.

[Official code, lines 396–410](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L396-L410).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicestatus-getiopwm"></a>

#### `GetIoPWM(pin)`

Returns `data`: duty cycle in %. For raw < 65535 source computes `float(raw)*100//65534` (floor division, normally a whole-valued float); raw 65535 returns integer 100. Manufacturer README fractional example does not describe this pinned implementation exactly.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 412–422](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L412-L422).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

### PiJuiceRtcAlarm (6)

<a id="pijuicertcalarm-getcontrolstatus"></a>

#### `GetControlStatus()`

Returns `data`: object `alarm_wakeup_enabled`, `alarm_flag` (bool). Enabled requires both control bits 0 and 2 set; alarm_flag reflects status bit 0.

[Official code, lines 441–455](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L441-L455).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicertcalarm-setwakeupenabled"></a>

#### `SetWakeupEnabled(status)`

Reads the current setting, then updates and checks it if needed. Returns the usual success dictionary immediately if already in the requested state. Enables/disables RTC alarm wakeup using status compared with True/False. Success does not prove that a system will physically wake.

[Official code, lines 468–483](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L468-L483).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicertcalarm-gettime"></a>

#### `GetTime()`

Returns `data`: object `second`, `minute`, `day`, `month`, `year`, `weekday` (integers); `hour` is an integer in 24-hour mode or a string such as "7 PM" in 12-hour mode. Year is decoded +2000; weekday is the raw low three bits, no locale name. `subsecond` is `byte//256`, hence always 0 for a valid byte in this revision. `daylightsaving` = SUB1H / ADD1H / NONE; `storeoperation` bool. No timezone/UTC offset is returned.

[Official code, lines 485–524](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L485-L524).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicertcalarm-settime"></a>

#### `SetTime(dateTime)`

Custom verified write: the usual success dictionary or WRITE_FAILED after read-back (with limited seconds/subsecond tolerance). Accepts time fields from GetTime. Missing fields are encoded as zero, not preserved; None/{} also writes zero fields. Validation permits second/minute 0–60, weekday 1–7, day 1–31, month 1–12, year 2000–2099; hour supports 0–23 or AM/PM strings. `subsecond` uses `int(value)*256` then checks 0–255, so normal nonzero fractions cannot be represented. DST/store fields are encoded flags. These are source behaviors, not a guarantee of calendar validity.

Errors mentioned in the code: `INVALID_DAY`, `INVALID_HOUR`, `INVALID_MINUTE`, `INVALID_MONTH`, `INVALID_SECOND`, `INVALID_SUBSECOND`, `INVALID_WEEKDAY`, `INVALID_YEAR`, `WRITE_FAILED`.

[Official code, lines 526–664](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L526-L664).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicertcalarm-getalarm"></a>

#### `GetAlarm()`

Returns `data`: variable object. `second` is omitted when its mask bit is set. Either `minute` (integer) or `minute_period` (raw byte, minutes) is returned. `hour` is an integer, AM/PM string, EVERY_HOUR, or semicolon-delimited hour string (possibly empty). Either `weekday` (integer, EVERY_DAY, or semicolon-delimited numbers) or `day` (integer / EVERY_DAY) is returned. No month/year/timezone. The multi-hour 12-hour string construction has unusual index arithmetic; do not normalise it into an assumed corrected schedule.

[Official code, lines 666–733](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L666-L733).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicertcalarm-setalarm"></a>

#### `SetAlarm(alarm)`

Custom verified write: the usual success dictionary or WRITE_FAILED after read-back and hour-format comparison. None/{} follows the branch commented "disable alarm"; this does not itself call SetWakeupEnabled(False). Supports second/minute (source accepts 0–60), minute_period (1–60), hour (integer / AM-PM / EVERY_HOUR / semicolon list), weekday or day (EVERY_DAY or numeric forms; weekday also list). Weekday takes precedence over day. Manufacturer notes minute_period is aligned within each hour (e.g. 5 → :00,:05,…,:55), largest meaningful value 30; it is not an elapsed-duration timer. Source validation is incomplete for hour/day/weekday.

Errors mentioned in the code: `INVALID_DAY_OF_MONTH`, `INVALID_HOUR`, `INVALID_MINUTE`, `INVALID_MINUTE_PERIOD`, `INVALID_SECOND`, `INVALID_WEEKDAY`, `WRITE_FAILED`.

[Official code, lines 735–908](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L735-L908).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

### PiJuicePower (8)

<a id="pijuicepower-setpoweroff"></a>

#### `SetPowerOff(delay)`

Returns `{'error': 'NO_ERROR'}` after writing. delay is seconds in the official notes. Removes PiJuice power to GPIO after delay; does not itself perform an OS shutdown. Source sends `[delay]` without range validation. Special byte values beyond this description are not confirmed here.

[Official code, lines 928–929](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L928-L929).

**Test result:** An earlier user report describes a successful controlled SetPowerOff(60) plus OS halt test, with the power LED turning off. This is a user-reported physical result consistent with the manufacturer's delayed power-cut feature; no direct setter return dictionary or measured 60-second timing was retained in the evidence used here. It does not validate automatic recharge wakeup or every power-input arrangement.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicepower-getpoweroff"></a>

#### `GetPowerOff()`

Returns `data`: one-element byte list `[delay]`, not a scalar; manufacturer defines power-off delay in seconds. The reviewed wrapper does not confirm whether the returned register is a countdown or the original setting, nor special-value meanings.

[Official code, lines 931–932](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L931-L932).

**Test result:** Earlier output: `{'data': [255], 'error': 'NO_ERROR'}`. Matches the one-element list shape. The reviewed API prose does not document the special meaning of 255; retain it as a raw register value rather than calling it a 255-second countdown or asserting that it means disabled.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicepower-setwakeuponcharge"></a>

#### `SetWakeUpOnCharge(arg, non_volatile=False)`

Returns `{'error': 'NO_ERROR'}` after writing. arg is DISABLED or integer-convertible charge threshold 0–100%; optional non_volatile controls bit 7. Important source gap: an out-of-range numeric arg leaves `d` unassigned and can raise UnboundLocalError, rather than returning BAD_ARGUMENT.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 934–943](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L934-L943).

**Test result:** An earlier call to SetWakeUpOnCharge(40, True) returned `{'error': 'NO_ERROR'}`; subsequent getter returned data 40 and outer non_volatile True. Write and immediate read-back shapes agree with source. This does not prove persistence across complete power loss or actual automatic restart at 40%.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicepower-getwakeuponcharge"></a>

#### `GetWakeUpOnCharge()`

Returns `data` and a separate `non_volatile` boolean: data is DISABLED when low 7 bits = 127, otherwise integer threshold %. Source does not reject other out-of-range codes.

[Official code, lines 945–954](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L945-L954).

**Test result:** Earlier output: `{'data': 40, 'non_volatile': True, 'error': 'NO_ERROR'}`. Matches the source's scalar percentage and outer persistence flag. It verifies a reported setting, not completion of a recharge-triggered wakeup test.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicepower-setwatchdog"></a>

#### `SetWatchdog(minutes, non_volatile=False)`

Returns `{'error': 'NO_ERROR'}` after writing. minutes: manufacturer 0 disables, 1–65535 activates timeout in minutes; optional non_volatile bit. Source masks to 16 bits instead of range-checking. Values >=16384 use four-minute resolution, discarding low two bits.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 957–965](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L957-L965).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicepower-getwatchdog"></a>

#### `GetWatchdog()`

Returns `data` and a separate `non_volatile` boolean. data is integer configured watchdog minutes, 0 disabled. Low 14 bits decoded at 1- or 4-minute resolution according to bit 14; not a remaining-time claim.

[Official code, lines 967–976](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L967-L976).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicepower-setsystempowerswitch"></a>

#### `SetSystemPowerSwitch(state)`

Returns `{'error': 'NO_ERROR'}` after writing. VSYS output current limit in mA: manufacturer options 0 (off), 500, 2100. Source sends `int(state)//100`, without enforcing that option set.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 978–983](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L978-L983).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuicepower-getsystempowerswitch"></a>

#### `GetSystemPowerSwitch()`

Returns `data`: integer configured VSYS current limit in mA (register byte × 100); 0 means off. This is a setting, not measured load current.

[Official code, lines 985–990](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L985-L990).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

### PiJuiceConfig (32)

<a id="pijuiceconfig-setchargingconfig"></a>

#### `SetChargingConfig(config, non_volatile=False)`

Returns `{'error': 'NO_ERROR'}` after writing and checking the bytes. config is bool or object with `charging_enabled` bool; optional non_volatile. Special case: if non_volatile == False, WRITE_FAILED is changed to NO_ERROR (upstream comment: configuration matches EEPROM). Do not interpret this success as unconditional byte-for-byte verification.

Errors mentioned in the code: `BAD_ARGUMENT`, `WRITE_FAILED`.

[Official code, lines 1022–1041](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1022-L1041).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getchargingconfig"></a>

#### `GetChargingConfig()`

Returns `data` and a separate `non_volatile` boolean; data object contains `charging_enabled` bool.

[Official code, lines 1043–1049](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1043-L1049).

**Test result:** Earlier output: `{'data': {'charging_enabled': True}, 'non_volatile': False, 'error': 'NO_ERROR'}`. Matches the source's nested data and outer persistence flag. Manufacturer example uses non_volatile True; that different setting is not a schema discrepancy. Enabled does not guarantee that charge current is flowing.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setbatteryprofile"></a>

#### `SetBatteryProfile(profile)`

Returns `{'error': 'NO_ERROR'}` after writing. Selects DEFAULT, CUSTOM, or a name in the instance batteryProfiles list. Available names/order depend on firmware profile selection; the installed names alone do not establish firmware compatibility.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1062–1073](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1062-L1073).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getbatteryprofilestatus"></a>

#### `GetBatteryProfileStatus()`

Returns `data`: normally object `validity` VALID/INVALID, `source` HOST/DIP_SWITCH/RESISTOR, `origin` CUSTOM/PREDEFINED, `profile` selected name or UNKNOWN. Byte 0xF0 instead returns only `{validity: DATA_WRITE_NOT_COMPLETED}` with NO_ERROR. Reserved source index 3 is not caught and may raise IndexError.

[Official code, lines 1077–1093](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1077-L1093).

**Test result:** Earlier output: `{'data': {'validity': 'VALID', 'source': 'DIP_SWITCH', 'origin': 'PREDEFINED', 'profile': 'BP7X_1820'}, 'error': 'NO_ERROR'}`. The fields and values match the code. VALID is a firmware-reported profile state, not independent verification of the fitted battery.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getbatteryprofile"></a>

#### `GetBatteryProfile()`

Returns `data`: [BatteryProfile](#batteryprofile) object, or string INVALID when all 14 bytes are zero. INVALID is a data value with NO_ERROR, not a transport error.

[Official code, lines 1095–1116](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1095-L1116).

**Test result:** Earlier `data` value: `{'capacity': 1820, 'chargeCurrent': 925, 'terminationCurrent': 50, 'regulationVoltage': 4180, 'cutoffVoltage': 3000, 'tempCold': 1, 'tempCool': 10, 'tempWarm': 45, 'tempHot': 59, 'ntcB': 3380, 'ntcResistance': 10000}`, with outer error NO_ERROR. All eleven fields match the source schema and the manufacturer README BP7X example. These are configured profile parameters, not measured cell characteristics.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setcustombatteryprofile"></a>

#### `SetCustomBatteryProfile(profile)`

Writes the setting, waits 0.2 seconds and checks the bytes. Returns the usual success/error dictionary. Requires all [BatteryProfile](#batteryprofile) fields; encodes/quantises them, rather than guaranteeing exact round-trip input values. Capacity is capped at 4194175 and uses coarse packing above 32767; 0xFFFFFFFF is encoded as 0xFFFF. Temperatures wrap to unsigned bytes for transfer. Application must check physical suitability separately.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1118–1145](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1118-L1145).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getbatteryextprofile"></a>

#### `GetBatteryExtProfile()`

Returns `data`: [ExtendedProfile](#extendedprofile) object, or string INVALID when all 17 bytes are zero. Reads 17 bytes but exposes decoded fields only through byte 12; chemistry unknown → UNKNOWN.

[Official code, lines 1148–1167](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1148-L1167).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setcustombatteryextprofile"></a>

#### `SetCustomBatteryExtProfile(profile)`

Writes the setting, waits 0.2 seconds and checks the bytes. Returns the usual success/error dictionary. Requires chemistry, ocv10/50/90, r10/50/90. chemistry must be LIPO/LIFEPO4; ocv values converted with int and masked to 16 bits; r values multiplied by 100, truncated and masked to 16 bits. Writes last four bytes as 0xFF. No complete physical range validation.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1169–1198](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1169-L1198).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getbatterytempsenseconfig"></a>

#### `GetBatteryTempSenseConfig()`

Returns `data`: NOT_USED / NTC / ON_BOARD / AUTO_DETECT. Other low-three-bit codes return UNKNOWN_DATA. ON_BOARD is the MCU sensor; AUTO_DETECT delegates selection.

Errors mentioned in the code: `UNKNOWN_DATA`.

[Official code, lines 1201–1210](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1201-L1210).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setbatterytempsenseconfig"></a>

#### `SetBatteryTempSenseConfig(config)`

Reads the current setting, then writes and checks it, preserving unrelated register bits. Accepts NOT_USED / NTC / ON_BOARD / AUTO_DETECT. Unknown option raises ValueError from list.index; the written BAD_ARGUMENT check is ineffective for that case.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1212–1220](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1212-L1220).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getrsocestimationconfig"></a>

#### `GetRsocEstimationConfig()`

Returns `data`: AUTO_DETECT / DIRECT_BY_MCU. Other two-bit codes return UNKNOWN_DATA. Names identify estimation configuration; algorithm accuracy is not established by this getter.

Errors mentioned in the code: `UNKNOWN_DATA`.

[Official code, lines 1223–1232](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1223-L1232).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setrsocestimationconfig"></a>

#### `SetRsocEstimationConfig(config)`

Reads the current setting, then writes and checks it; preserves unrelated bits. Accepts AUTO_DETECT / DIRECT_BY_MCU. Unknown option raises ValueError from list.index, rather than reaching the BAD_ARGUMENT check.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1234–1242](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1234-L1242).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setpowerinputsconfig"></a>

#### `SetPowerInputsConfig(config, non_volatile=False)`

Returns `{'error': 'NO_ERROR'}` after writing and checking the bytes. Requires [PowerInputs](#powerinputs) fields; optional non_volatile. Invalid current-limit/DPM names actually produce BAD_ARGUMENT via caught ValueError, not the INVALID_USB_MICRO_* checks placed after list.index. Unknown precedence silently maps to USB_MICRO.

Errors mentioned in the code: `BAD_ARGUMENT`, `INVALID_USB_MICRO_CURRENT_LIMIT`, `INVALID_USB_MICRO_DPM`.

[Official code, lines 1247–1266](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1247-L1266).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getpowerinputsconfig"></a>

#### `GetPowerInputsConfig()`

Returns `data` and a separate `non_volatile` boolean. data is [PowerInputs](#powerinputs) object.

[Official code, lines 1268–1280](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1268-L1280).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getbuttonconfiguration"></a>

#### `GetButtonConfiguration(button)`

Returns `data`: object keyed by PRESS, RELEASE, SINGLE_PRESS, DOUBLE_PRESS, LONG_PRESS1, LONG_PRESS2, each `{function: str, parameter: int}`. parameter is byte × 100 ms in the official notes; its use depends on the assigned function/event. Function can be NO_FUNC, a hardware/system/user function, or UNKNOWN. button is SW1/SW2/SW3.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1285–1313](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1285-L1313).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setbuttonconfiguration"></a>

#### `SetButtonConfiguration(button, config)`

Writes the setting, waits 0.4 seconds and checks the bytes. Returns the usual success/error dictionary. button SW1/SW2/SW3; requires all six event objects from GetButtonConfiguration, each function and parameter. Parameter encoded `(int(parameter)//100)&255` (ms). Unknown function names eventually encode NO_FUNC; missing fields/type errors may escape as Python exceptions.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1315–1337](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1315-L1337).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getledconfiguration"></a>

#### `GetLedConfiguration(led)`

Returns `data`: `{function: str, parameter: {r: int, g: int, b: int}}`; brightness bytes 0–255. function = NOT_USED / CHARGE_STATUS / ON_OFF_STATUS / USER_LED; unknown code returns UNKNOWN_CONFIG. led D1/D2.

Errors mentioned in the code: `BAD_ARGUMENT`, `UNKNOWN_CONFIG`.

[Official code, lines 1343–1363](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1343-L1363).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setledconfiguration"></a>

#### `SetLedConfiguration(led, config)`

Writes the setting, waits 0.2 seconds and checks the bytes. Returns the usual success/error dictionary. D1/D2 with function and RGB parameter object as above. Source comment advises avoiding ON_OFF_STATUS even though its enum accepts it. Only ValueError is caught; missing keys/type errors may raise exceptions. No complete RGB range validation.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1365–1376](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1365-L1376).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getpowerregulatormode"></a>

#### `GetPowerRegulatorMode()`

Returns `data`: POWER_SOURCE_DETECTION / LDO / DCDC. Unknown byte returns UNKNOWN_DATA.

Errors mentioned in the code: `UNKNOWN_DATA`.

[Official code, lines 1379–1388](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1379-L1388).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setpowerregulatormode"></a>

#### `SetPowerRegulatorMode(mode)`

Returns `{'error': 'NO_ERROR'}` after writing and checking the bytes. Accepts POWER_SOURCE_DETECTION / LDO / DCDC; unknown name → BAD_ARGUMENT.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1390–1395](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1390-L1395).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getrunpinconfig"></a>

#### `GetRunPinConfig()`

Returns `data`: NOT_INSTALLED / INSTALLED; unknown byte returns UNKNOWN_DATA. Reports configuration, not physical inspection of a fitted pin.

Errors mentioned in the code: `UNKNOWN_DATA`.

[Official code, lines 1399–1408](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1399-L1408).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setrunpinconfig"></a>

#### `SetRunPinConfig(config)`

Returns `{'error': 'NO_ERROR'}` after writing and checking the bytes. Accepts NOT_INSTALLED / INSTALLED; unknown name → BAD_ARGUMENT.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1410–1415](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1410-L1415).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setioconfiguration"></a>

#### `SetIoConfiguration(io_pin, config, non_volatile=False)`

Writes the setting, waits 0.2 seconds and checks the bytes. Returns the usual success/error dictionary. Mode-specific [IoConfiguration](#ioconfiguration) object; optional non_volatile. PWM period below 2 → INVALID_PERIOD; duty outside 0–100 or caught conversion/key errors → INVALID_CONFIG. Period upper bound and io_pin 1/2 are not validated here; oversized periods wrap into two bytes. Source supported-modes metadata excludes ANALOG_IN on IO2.

Errors mentioned in the code: `INVALID_CONFIG`, `INVALID_PERIOD`.

[Official code, lines 1437–1469](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1437-L1469).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getioconfiguration"></a>

#### `GetIoConfiguration(io_pin)`

Returns `data` and a separate `non_volatile` boolean; data is the mode-specific [IoConfiguration](#ioconfiguration) object. io_pin is used in register arithmetic without explicit pin validation.

[Official code, lines 1471–1492](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1471-L1492).

**Test result:** Calling without io_pin gave `TypeError: PiJuiceConfig.GetIoConfiguration() missing 1 required positional argument: 'io_pin'`. This agrees with the required source argument; it is not an I2C error dictionary. No successful pin-specific return object was located in the earlier test notes.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getaddress"></a>

#### `GetAddress(slave)`

Returns `data`: lowercase hexadecimal string without 0x or fixed-width padding, for slave 1/2; e.g. "14". Reads configuration register, unlike interface.GetAddress().

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1494–1501](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1494-L1501).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setaddress"></a>

#### `SetAddress(slave, hexAddress)`

Returns `{'error': 'NO_ERROR'}` after writing. slave 1/2, address parsed as `int(str(hexAddress),16)` then checked 0–0x7F. Pass a hex string to avoid decimal/hex ambiguity. This method does not update the interface cached address.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1503–1511](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1503-L1511).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getideepromwriteprotect"></a>

#### `GetIdEepromWriteProtect()`

Returns `data`: bool, True only when the byte equals 1; every other byte maps to False.

[Official code, lines 1513–1519](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1513-L1519).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setideepromwriteprotect"></a>

#### `SetIdEepromWriteProtect(status)`

Returns `{'error': 'NO_ERROR'}` after writing and checking the bytes. status compared with True/False; otherwise BAD_ARGUMENT. No data returned.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1521–1529](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1521-L1529).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getideepromaddress"></a>

#### `GetIdEepromAddress()`

Returns `data`: lowercase hexadecimal string, no 0x prefix or padding. Reads byte and formats it; does not restrict observed values to the setter allowlist.

[Official code, lines 1532–1537](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1532-L1537).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setideepromaddress"></a>

#### `SetIdEepromAddress(hexAddress)`

Returns `{'error': 'NO_ERROR'}` after writing and checking the bytes. accepts values whose string is exactly "50" or "52", interpreted as hexadecimal I2C addresses. Other forms, including "0x50", return BAD_ARGUMENT.

Errors mentioned in the code: `BAD_ARGUMENT`.

[Official code, lines 1539–1544](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1539-L1544).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-setdefaultconfiguration"></a>

#### `SetDefaultConfiguration()`

Returns `{'error': 'NO_ERROR'}` after writing. Sends reset-to-default command sequence. No returned configuration and no read-back verification; success only means the transport write completed.

[Official code, lines 1546–1547](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1546-L1547).

**Test result:** No test result recorded.

[↑ Back to API Inventory](#pijuice-api-inventory)

<a id="pijuiceconfig-getfirmwareversion"></a>

#### `GetFirmwareVersion()`

Returns `data`: `{version: str, variant: str}`. version is decimal text of high/low nibbles of byte 0 (e.g. "1.6"); variant is lowercase hex string of byte 1 without 0x/padding. Firmware version is distinct from Python module __version__ = "1.8".

[Official code, lines 1549–1560](https://github.com/PiSupply/PiJuice/blob/df8674691bd376170cfc4659d8f2e2fbebed29b3/Software/Source/pijuice.py#L1549-L1560).

**Test result:** Earlier output: `{'data': {'version': '1.5', 'variant': '0'}, 'error': 'NO_ERROR'}`. String fields agree with decoding. This establishes the reported firmware at that historical test only, not its present version, nor the Python module revision used for every other sample.

[↑ Back to API Inventory](#pijuice-api-inventory)

## Interpretation limits

NO_ERROR is a library operation result. It does not guarantee a valid battery profile, a connected battery, charging safety, future wakeup, or successful OS shutdown. INVALID profile strings and DATA_WRITE_NOT_COMPLETED validity are data states even when error is NO_ERROR. Configuration values and current limits are settings, not measurements.

The test results below are from earlier records. They do not show the current device state. Any further hardware test needs separate approval and should record the library and firmware versions. Some functions may depend on the firmware version.
