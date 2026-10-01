#!/usr/bin/env python3

import html
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from pijuice_reader import read_snapshot


HOST = "0.0.0.0"
PORT = 8080


def build_page():
    try:
        reading = read_snapshot()
        error = None
    except RuntimeError as exc:
        reading = None
        error = str(exc)

    updated = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    if error:
        content = f"""
        <div class="error">
            Unable to read PiJuice: {html.escape(error)}
        </div>
        """
    else:
        temp_class = (
            "warning"
            if reading["temperature_status"] == "ANOMALY"
            else "normal"
        )

        fault_class = "warning" if reading["fault"] else "normal"

        content = f"""
        <div class="grid">
            <div class="card">
                <div class="label">Battery</div>
                <div class="value">{reading["charge"]}%</div>
            </div>

            <div class="card">
                <div class="label">Battery state</div>
                <div class="value small">{html.escape(str(reading["battery"]))}</div>
            </div>

            <div class="card">
                <div class="label">External power</div>
                <div class="value small">{html.escape(str(reading["power_input"]))}</div>
            </div>

            <div class="card">
                <div class="label">Voltage</div>
                <div class="value">{reading["voltage"]:.3f} V</div>
            </div>

            <div class="card">
                <div class="label">Temperature</div>
                <div class="value">{reading["temperature"]}°C</div>
                <div class="status {temp_class}">
                    {reading["temperature_status"]}
                </div>
            </div>

            <div class="card">
                <div class="label">Fault</div>
                <div class="value small">{reading["fault"]}</div>
                <div class="status {fault_class}">
                    {"FAULT" if reading["fault"] else "OK"}
                </div>
            </div>
        </div>
        """

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="5">
<title>PiJuice Monitor</title>

<style>
    body {{
        margin: 0;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f4f5f7;
        color: #202124;
    }}

    .container {{
        max-width: 900px;
        margin: 0 auto;
        padding: 32px 20px;
    }}

    h1 {{
        margin-bottom: 6px;
    }}

    .subtitle {{
        color: #666;
        margin-bottom: 28px;
    }}

    .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
    }}

    .card {{
        background: white;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.07);
    }}

    .label {{
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }}

    .value {{
        font-size: 2rem;
        font-weight: 650;
    }}

    .value.small {{
        font-size: 1.25rem;
        word-break: break-word;
    }}

    .status {{
        display: inline-block;
        margin-top: 12px;
        padding: 5px 9px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 700;
    }}

    .normal {{
        background: #e8f5e9;
        color: #1b5e20;
    }}

    .warning {{
        background: #fff3e0;
        color: #b45309;
    }}

    .error {{
        background: white;
        border-radius: 14px;
        padding: 22px;
        color: #b00020;
    }}

    footer {{
        margin-top: 28px;
        color: #777;
        font-size: 0.85rem;
    }}
</style>
</head>

<body>
<div class="container">

    <h1>PiJuice Monitor</h1>
    <div class="subtitle">Raspberry Pi 3B+ Power Monitor</div>

    {content}

    <footer>
        Last updated: {html.escape(updated)}<br>
        Auto refresh: 5 seconds
    </footer>

</div>
</body>
</html>
"""


class DashboardHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return

        page = build_page().encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

        self.wfile.write(page)

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer((HOST, PORT), DashboardHandler)

    print("PiJuice Web Dashboard")
    print("---------------------")
    print(f"Listening on : http://{HOST}:{PORT}")
    print(f"LAN address  : http://<raspberry-pi-hostname>.local:{PORT}")
    print()
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
