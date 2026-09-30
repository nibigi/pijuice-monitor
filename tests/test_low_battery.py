import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from low_battery_monitor import (
    decide_action,
    confirm_low_battery,
    schedule_safe_shutdown,
)

def test_low_battery_without_power():
    action, _ = decide_action(15, "NOT_PRESENT")
    assert action == "SHUTDOWN CANDIDATE"


def test_low_battery_with_power():
    action, _ = decide_action(15, "PRESENT")
    assert action == "KEEP RUNNING"


def test_normal_battery_without_power():
    action, _ = decide_action(50, "NOT_PRESENT")
    assert action == "KEEP RUNNING"


def test_confirm_continuous_low_battery():
    readings = iter([
        (15, "NOT_PRESENT"),
        (15, "NOT_PRESENT"),
        (15, "NOT_PRESENT"),
    ])

    result = confirm_low_battery(
        lambda: next(readings),
        sleep_fn=lambda seconds: None,
    )

    assert result is True


def test_cancel_when_battery_recovers():
    readings = iter([
        (15, "NOT_PRESENT"),
        (15, "NOT_PRESENT"),
        (25, "NOT_PRESENT"),
    ])

    result = confirm_low_battery(
        lambda: next(readings),
        sleep_fn=lambda seconds: None,
    )

    assert result is False


def test_cancel_when_power_returns():
    readings = iter([
        (15, "NOT_PRESENT"),
        (15, "PRESENT"),
    ])

    result = confirm_low_battery(
        lambda: next(readings),
        sleep_fn=lambda seconds: None,
    )

    assert result is False


def test_safe_shutdown_dry_run():
    status, message = schedule_safe_shutdown(None, dry_run=True)

    assert status == "DRY RUN"
    assert "60 seconds" in message


def test_safe_shutdown_schedules_power_off():
    class FakePower:
        def __init__(self):
            self.delay = None

        def SetPowerOff(self, delay):
            self.delay = delay
            return {"error": "NO_ERROR"}

    class FakePiJuice:
        def __init__(self):
            self.power = FakePower()

    pj = FakePiJuice()

    status, _ = schedule_safe_shutdown(pj, dry_run=False)

    assert status == "SHUTDOWN SCHEDULED"
    assert pj.power.delay == 60


def test_safe_shutdown_power_off_failure():
    class FakePower:
        def SetPowerOff(self, delay):
            return {"error": "COMMUNICATION_ERROR"}

    class FakePiJuice:
        def __init__(self):
            self.power = FakePower()

    pj = FakePiJuice()

    status, message = schedule_safe_shutdown(pj, dry_run=False)

    assert status == "ERROR"
    assert "Unable to schedule PiJuice power-off" in message


if __name__ == "__main__":
    test_low_battery_without_power()
    test_low_battery_with_power()
    test_normal_battery_without_power()

    test_confirm_continuous_low_battery()
    test_cancel_when_battery_recovers()
    test_cancel_when_power_returns()

    test_safe_shutdown_dry_run()
    test_safe_shutdown_schedules_power_off()
    test_safe_shutdown_power_off_failure()

    print("All low-battery tests passed.")
