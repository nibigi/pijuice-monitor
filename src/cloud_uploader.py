import json
import os
import urllib.error
import urllib.request

from pijuice_reader import read_snapshot


CLOUD_URL = "https://pijuice-monitor.duckdns.org/api/telemetry"
DEVICE_ID = "pijuice-main"


def upload_snapshot():
    snapshot = read_snapshot()
    snapshot["device_id"] = DEVICE_ID

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

if __name__ == "__main__":
    upload_snapshot()
