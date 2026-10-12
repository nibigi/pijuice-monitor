import json
import os
import urllib.error
import urllib.request

from pijuice_reader import read_snapshot


CLOUD_URL = "https://pijuice-monitor.duckdns.org/api/telemetry"
DEVICE_ID = "pijuice-main"


def upload_snapshot():
    snapshot = build_v2_payload()

    token = os.environ["PIJUICE_API_TOKEN"]

    request = urllib.request.Request(
        CLOUD_URL,
        data=json.dumps(snapshot).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-API-Token": token,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            print(response.read().decode("utf-8"))
            return True
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"Upload failed: {exc}")
        return False



def build_v2_payload():
    """Build Schema v2 telemetry without uploading it."""
    from pijuice_reader import read_extended_battery

    snapshot = read_snapshot()
    snapshot["device_id"] = DEVICE_ID
    snapshot["schema_version"] = 2
    snapshot["payload_json"] = {
        "battery_extended": read_extended_battery()
    }

    try:
        from system_reader import read_system_snapshot
        snapshot["payload_json"]["system"] = read_system_snapshot()
    except Exception as exc:
        snapshot["payload_json"]["system"] = {
            "error": str(exc)
        }

    try:
        from led_reader import read_leds
        snapshot["payload_json"]["leds"] = read_leds()
    except Exception as exc:
        snapshot["payload_json"]["leds"] = {"error": str(exc)}

    return snapshot


if __name__ == "__main__":
    upload_snapshot()
