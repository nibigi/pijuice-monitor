import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from low_battery_monitor import decide_action, confirm_low_battery

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


if __name__ == "__main__":
    test_low_battery_without_power()
    test_low_battery_with_power()
    test_normal_battery_without_power()

    test_confirm_continuous_low_battery()
    test_cancel_when_battery_recovers()
    test_cancel_when_power_returns()

    print("All low-battery tests passed.")
