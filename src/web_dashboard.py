#!/usr/bin/env python3

import csv
import html
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from pijuice_reader import read_snapshot


HOST = "0.0.0.0"
PORT = 8080

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HISTORY_FILE = PROJECT_ROOT / "data" / "pijuice_history.csv"
HISTORY_LIMIT = 240


def read_history(limit=HISTORY_LIMIT):
    if not HISTORY_FILE.exists():
        return []

    with HISTORY_FILE.open(newline="") as file:
        rows = list(csv.DictReader(file))

    history = []

    for row in rows[-limit:]:
        try:
            history.append(
                {
                    "timestamp": row["timestamp"],
                    "charge": int(row["charge"]),
                    "voltage": float(row["voltage"]),
                    "temperature": int(row["temperature"]),
                    "temperature_status": row["temperature_status"],
                    "battery": row["battery"],
                    "power_input": row["power_input"],
                    "fault": row["fault"].lower() == "true",
                }
            )
        except (KeyError, TypeError, ValueError):
            continue

    return history


def build_page():
    try:
        reading = read_snapshot()
        error = None
    except RuntimeError as exc:
        reading = None
        error = str(exc)

    updated = datetime.now().astimezone().strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )

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
        <div class="value" id="battery-charge">{reading["charge"]}%</div>
            </div>

            <div class="card">
                <div class="label">Battery state</div>
                <div class="value small"  id="battery-state">
                    {html.escape(str(reading["battery"]))}
                </div>
            </div>

            <div class="card">
                <div class="label">External power</div>
                <div class="value small"  id="external-power">
                    {html.escape(str(reading["power_input"]))}
                </div>
            </div>

            <div class="card">
                <div class="label">Voltage</div>
                <div class="value" id="voltage">{reading["voltage"]:.3f} V</div>
            </div>

            <div class="card">
                <div class="label">Temperature</div>
                <div class="value" id="temperature">{reading["temperature"]}°C</div>
                <div class="status {temp_class}"  id="temperature-status">
                    {reading["temperature_status"]}
                </div>
            </div>

            <div class="card">
                <div class="label">Fault</div>
                <div class="value small" id="fault-value">{reading["fault"]}</div>
                <div class="status {fault_class}" id="fault-status">
                    {"FAULT" if reading["fault"] else "OK"}
                </div>
            </div>
        </div>
        """

    page = """<!doctype html>
<html lang="en">

<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>PiJuice Monitor</title>

<style>
body {
    margin: 0;
    font-family:
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
    background: #f4f5f7;
    color: #202124;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 32px 20px;
}

h1 {
    margin-bottom: 6px;
}

.subtitle {
    color: #666;
    margin-bottom: 28px;
}

.grid {
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
}

.card {
    background: white;
    border-radius: 14px;
    padding: 22px;
    box-shadow:
        0 2px 10px rgba(0, 0, 0, 0.07);
}

.label {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 8px;
}

.value {
    font-size: 2rem;
    font-weight: 650;
}

.value.small {
    font-size: 1.25rem;
    word-break: break-word;
}

.status {
    display: inline-block;
    margin-top: 12px;
    padding: 5px 9px;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 700;
}

.normal {
    background: #e8f5e9;
    color: #1b5e20;
}

.warning {
    background: #fff3e0;
    color: #b45309;
}

.error {
    background: white;
    border-radius: 14px;
    padding: 22px;
    color: #b00020;
}

.history-section {
    margin-top: 32px;
}

.history-section h2 {
    margin-bottom: 16px;
}

.chart-card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow:
        0 2px 10px rgba(0, 0, 0, 0.07);
}

#battery-chart {
    display: block;
    width: 100%;
    height: auto;
}

.chart-grid {
    stroke: #e5e7eb;
    stroke-width: 1;
}

.chart-label {
    fill: #6b7280;
}

.chart-line {
    fill: none;
    stroke: #2563eb;
    stroke-width: 3;
    stroke-linejoin: round;
    stroke-linecap: round;
}

.chart-label {
    fill: #777;
    font-size: 12px;
}

.chart-info {
    margin-top: 12px;
    color: #777;
    font-size: 0.85rem;
}

footer {
    margin-top: 28px;
    color: #777;
    font-size: 0.85rem;
}
</style>
</head>

<body>

<div class="container">

    <h1>PiJuice Monitor</h1>

    <div class="subtitle">
        Raspberry Pi 3B+ Power Monitor
    </div>

    __CONTENT__

    <section class="history-section">

        <h2>Battery History</h2>

        <div class="chart-card">

            <svg
                id="battery-chart"
                viewBox="0 0 800 260"
                role="img"
                aria-label="Battery charge history">
            </svg>

            <div
                id="battery-chart-info"
                class="chart-info">
                Loading historical data...
            </div>

        </div>

    </section>

<section class="history-section">

    <h2>Voltage History</h2>

    <div class="chart-card">

        <svg
            id="voltage-chart"
            viewBox="0 0 800 260"
            role="img"
            aria-label="Battery voltage history">
        </svg>

        <div
            id="voltage-chart-info"
            class="chart-info">
            Loading historical data...
        </div>

    </div>

</section>




    <footer>
        Last updated: <span id="last-updated">__UPDATED__</span><br>
        Live status refresh: 5 seconds<br>
        Historical sampling: 60 seconds
    </footer>

</div>

<script>
async function loadBatteryHistory() {

    const svg =
        document.getElementById("battery-chart");

    const info =
        document.getElementById("battery-chart-info");

    try {

        const response = await fetch(
            "/api/history",
            {cache: "no-store"}
        );

        if (!response.ok) {
            throw new Error(
                "HTTP " + response.status
            );
        }

        const history = await response.json();

        if (history.length < 2) {
            info.textContent =
                "Not enough historical data yet.";
            return;
        }

        const width = 800;
        const height = 260;

        const left = 70;
        const right = 20;
        const top = 20;
        const bottom = 40;

        const plotWidth =
            width - left - right;

        const plotHeight =
            height - top - bottom;

        const points = history.map(
            (row, index) => {

                const x =
                    left +
                    (
                        index /
                        (history.length - 1)
                    ) *
                    plotWidth;

                const y =
                    top +
                    (
                        (100 - row.charge) /
                        100
                    ) *
                    plotHeight;

                return (
                    x.toFixed(1) +
                    "," +
                    y.toFixed(1)
                );
            }
        ).join(" ");

        let grid = "";

        for (
            const charge
            of [0, 25, 50, 75, 100]
        ) {

            const y =
                top +
                (
                    (100 - charge) /
                    100
                ) *
                plotHeight;

            grid +=
                '<line ' +
                'class="chart-grid" ' +
                'x1="' + left + '" ' +
                'y1="' + y + '" ' +
                'x2="' +
                    (width - right) +
                    '" ' +
                'y2="' + y + '">' +
                '</line>';

            grid +=
                '<text ' +
                'class="chart-label" ' +

                'x="' +
                    (left - 8) +
                    '" ' +
                'y="' +
                    (y + 4) +
                    '" ' +
                'text-anchor="end">' +
                charge +
                '%' +
                '</text>';
        }

        svg.innerHTML =
            grid +
            '<polyline ' +
            'class="chart-line" ' +
            'points="' +
            points +
            '">' +
            '</polyline>';

        const first =
            new Date(history[0].timestamp);

        const last =
            new Date(
                history[
                    history.length - 1
                ].timestamp
            );

        info.textContent =
            history.length +
            " samples · " +
            first.toLocaleTimeString() +
            " – " +
            last.toLocaleTimeString();

    } catch (error) {

        info.textContent =
            "Unable to load historical data: " +
            error;
    }
}

async function loadVoltageHistory() {

    const info =
        document.getElementById("voltage-chart-info");

    try {
        const response = await fetch(
            "/api/history",
            {cache: "no-store"}
        );

        if (!response.ok) {
            throw new Error(
                "HTTP " + response.status
            );
        }

    const history = await response.json();

    const validHistory = history.filter(
        row => row.battery !== "NOT_PRESENT"
    );

    const startTime =
       new Date(validHistory[0].timestamp)
            .toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            second: "2-digit"
            });

    const endTime =
        new Date(validHistory[validHistory.length - 1].timestamp)
            .toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            second: "2-digit"
            });

    const svg = document.getElementById("voltage-chart");

    const voltages = validHistory.map(
        row => Number(row.voltage)
    );

    const minVoltage = Math.min(...voltages);
    const maxVoltage = Math.max(...voltages);
    const topLabel = maxVoltage.toFixed(2) + " V";
    const bottomLabel = minVoltage.toFixed(2) + " V";

    const width = 800;
    const height = 260;
    const padding = 30;
    const leftPadding = 70;
    const bottomPadding = 50;

    const gridMin = minVoltage;
    const gridMax = maxVoltage;
    const gridRange = gridMax - gridMin || 0.001;
    const gridStep = gridRange / 4;

    let grid = "";

    for (let i = 0; i < 5; i++) {

        const y =
            padding +
            i * (height - padding - bottomPadding) / 4;

	const voltage =
	    gridMax -
	    i * gridStep;

    grid +=
        '<line ' +
        'x1="' + leftPadding + '" ' +
        'y1="' + y + '" ' +
        'x2="' + (width - padding) + '" ' +
        'y2="' + y + '" ' +
        'class="chart-grid" />' +
        '<text x="5" y="' + (y + 5) + '" font-size="14" class="chart-label">' +
        voltage.toFixed(3) + ' V</text>';
    }

    const points = voltages.map((voltage, index) => {

        const x =
            leftPadding +
            index * (width - leftPadding - padding) /
            Math.max(voltages.length - 1, 1);

        const y =
            height - bottomPadding -
            (voltage - gridMin) *
            (height - padding - bottomPadding) /
            gridRange;

        return x + "," + y;

    }).join(" ");

    svg.innerHTML =
            grid +
            '<text x="' + leftPadding +
            '" y="' + (height - 5) +
        '" font-size="12">' +
        startTime +
        '</text>' +
        '<text x="' + (width - padding) +
        '" y="' + (height - 5) +
        '" font-size="12" text-anchor="end">' +
        endTime +
        '</text>' +
        '<polyline points="' + points +
        '" fill="none"' +
        ' stroke="#2563eb"' +
        ' stroke-width="3"' +
        ' stroke-linejoin="round"' +
        ' stroke-linecap="round" />';

    info.textContent =
        validHistory.length +
        " valid voltage samples loaded" +
        " | " +
        minVoltage.toFixed(3) +
        "–" +
        maxVoltage.toFixed(3) +
        " V";

    } catch (error) {
        info.textContent =
            "Unable to load voltage history: " +
            error;
    }
}

async function loadStatus() {

    try {
        const response = await fetch("/api/status");

        if (!response.ok) {
            throw new Error(
                "HTTP " + response.status
            );
        }

        const status = await response.json();

        document.getElementById(
            "battery-charge"
        ).textContent = status.charge + "%";

        document.getElementById(
            "voltage"
        ).textContent = status.voltage.toFixed(3) + " V";

        document.getElementById(
            "temperature"
        ).textContent = status.temperature + "°C";

        const temperatureStatus =
            document.getElementById("temperature-status");

        temperatureStatus.textContent =
            status.temperature_status;

        temperatureStatus.className =
            "status " +
            (status.temperature_status === "ANOMALY"
                ? "warning"
                : "normal");

        document.getElementById(
            "battery-state"
        ).textContent = status.battery;

        document.getElementById(
            "external-power"
        ).textContent = status.power_input;

        document.getElementById(
        "fault-value"
    ).textContent = status.fault ? "True" : "False";

    const faultStatus =
             document.getElementById("fault-status");

        faultStatus.textContent =
             status.fault ? "FAULT" : "OK";

        faultStatus.className =
             "status " +
             (status.fault ? "warning" : "normal");

        document.getElementById(
             "last-updated"
        ).textContent = new Date().toLocaleString();

    } catch (error) {
        console.error(
            "Unable to load PiJuice status:",
            error
        );
    }
}

loadBatteryHistory();
loadVoltageHistory();
loadStatus();
setInterval(loadStatus, 5000);
</script>

</body>
</html>
"""

    return (
        page
        .replace("__CONTENT__", content)
        .replace(
            "__UPDATED__",
            html.escape(updated),
        )
    )


class DashboardHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/api/status":

            try:
                status = read_snapshot()
                data = json.dumps(status).encode("utf-8")
            except RuntimeError as exc:
                data = json.dumps(
                    {"error": str(exc)}
                ).encode("utf-8")

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8",
            )

            self.send_header(
                "Content-Length",
                str(len(data)),
            )

            self.send_header(
                "Cache-Control",
                "no-store",
            )

            self.end_headers()

            self.wfile.write(data)
            return


        if self.path == "/api/history":

            data = json.dumps(
                read_history()
            ).encode("utf-8")

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8",
            )

            self.send_header(
                "Content-Length",
                str(len(data)),
            )

            self.send_header(
                "Cache-Control",
                "no-store",
            )

            self.end_headers()

            self.wfile.write(data)
            return

        if self.path not in (
            "/",
            "/index.html",
        ):
            self.send_error(404)
            return

        page = build_page().encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )

        self.send_header(
            "Content-Length",
            str(len(page)),
        )

        self.send_header(
            "Cache-Control",
            "no-store",
        )

        self.end_headers()

        self.wfile.write(page)

    def log_message(self, format, *args):
        return


def main():

    server = ThreadingHTTPServer(
        (HOST, PORT),
        DashboardHandler,
    )

    print("PiJuice Web Dashboard")
    print("---------------------")
    print(
        f"Listening on : "
        f"http://{HOST}:{PORT}"
    )

    print(
        f"LAN address  : "
        f"http://<raspberry-pi-hostname>.local:{PORT}"
    )
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
