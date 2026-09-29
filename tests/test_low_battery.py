import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from low_battery_monitor import decide_action


def test_low_battery_without_power():
    action, _ = decide_action(15, "NOT_PRESENT")
    assert action == "SHUTDOWN CANDIDATE"


def test_low_battery_with_power():
    action, _ = decide_action(15, "PRESENT")
    assert action == "KEEP RUNNING"


def test_normal_battery_without_power():
    action, _ = decide_action(50, "NOT_PRESENT")
    assert action == "KEEP RUNNING"

if __name__ == "__main__":
    test_low_battery_without_power()
    test_low_battery_with_power()
    test_normal_battery_without_power()

    print("All low-battery tests passed.")
