# PiJuice API inventory

Source: the user's AST extraction from
`/home/m0/PiJuice/Software/Source/pijuice.py` on the Raspberry Pi, supplied
with this release. The supplied label said 63, but the complete list totals
66 (1 + 19 + 6 + 8 + 32); all supplied names are retained.
This inventory records method names only, exactly as
observed: 66 class-method entries across five classes. GetAddress occurs in
two classes. No signatures, defaults, return shapes, units or behavior were
extracted, so none are asserted here. This is not a live hardware validation
or an inventory of every upstream PiJuice version.

Do not invoke Set methods during inventory or release checks. Confirm their
arguments and effects against the installed source before hardware use.

## PiJuiceInterface (1)

- `GetAddress`

## PiJuiceStatus (19)

- `GetStatus`
- `GetChargeLevel`
- `GetFaultStatus`
- `GetButtonEvents`
- `GetBatteryTemperature`
- `GetBatteryVoltage`
- `GetBatteryCurrent`
- `GetIoVoltage`
- `GetIoCurrent`
- `SetLedState`
- `GetLedState`
- `SetLedBlink`
- `GetLedBlink`
- `GetIoDigitalInput`
- `SetIoDigitalOutput`
- `GetIoDigitalOutput`
- `GetIoAnalogInput`
- `SetIoPWM`
- `GetIoPWM`

## PiJuiceRtcAlarm (6)

- `GetControlStatus`
- `SetWakeupEnabled`
- `GetTime`
- `SetTime`
- `GetAlarm`
- `SetAlarm`

## PiJuicePower (8)

- `SetPowerOff`
- `GetPowerOff`
- `SetWakeUpOnCharge`
- `GetWakeUpOnCharge`
- `SetWatchdog`
- `GetWatchdog`
- `SetSystemPowerSwitch`
- `GetSystemPowerSwitch`

## PiJuiceConfig (32)

- `SetChargingConfig`
- `GetChargingConfig`
- `SetBatteryProfile`
- `GetBatteryProfileStatus`
- `GetBatteryProfile`
- `SetCustomBatteryProfile`
- `GetBatteryExtProfile`
- `SetCustomBatteryExtProfile`
- `GetBatteryTempSenseConfig`
- `SetBatteryTempSenseConfig`
- `GetRsocEstimationConfig`
- `SetRsocEstimationConfig`
- `SetPowerInputsConfig`
- `GetPowerInputsConfig`
- `GetButtonConfiguration`
- `SetButtonConfiguration`
- `GetLedConfiguration`
- `SetLedConfiguration`
- `GetPowerRegulatorMode`
- `SetPowerRegulatorMode`
- `GetRunPinConfig`
- `SetRunPinConfig`
- `SetIoConfiguration`
- `GetIoConfiguration`
- `GetAddress`
- `SetAddress`
- `GetIdEepromWriteProtect`
- `SetIdEepromWriteProtect`
- `GetIdEepromAddress`
- `SetIdEepromAddress`
- `SetDefaultConfiguration`
- `GetFirmwareVersion`

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
