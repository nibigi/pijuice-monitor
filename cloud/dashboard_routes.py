import secrets
import json
import sqlite3
import time
from collections import defaultdict
from threading import Lock

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from dashboard_auth import verify_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")

_attempts = defaultdict(list)
_attempts_lock = Lock()
MAX_ATTEMPTS = 5
WINDOW_SECONDS = 900


def is_rate_limited(client_ip: str) -> bool:
    now = time.monotonic()
    with _attempts_lock:
        attempts = _attempts[client_ip]
        attempts[:] = [
            t for t in attempts if now - t < WINDOW_SECONDS
        ]
        return len(attempts) >= MAX_ATTEMPTS


def record_failure(client_ip: str):
    with _attempts_lock:
        _attempts[client_ip].append(time.monotonic())


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if request.session.get("authenticated"):
        return RedirectResponse("/dashboard", status_code=303)

    csrf_token = secrets.token_urlsafe(32)
    request.session["csrf_token"] = csrf_token

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": request.query_params.get("error") == "1", "csrf_token": csrf_token},
    )


@router.post("/login")
def login(
    request: Request,
    password: str = Form(...),
    csrf_token: str = Form(...),
):
    expected = request.session.get("csrf_token", "")
    if not expected or not secrets.compare_digest(csrf_token, expected):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    client_ip = request.client.host if request.client else "unknown"

    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Too many attempts")

    if not verify_password(password):
        record_failure(client_ip)
        request.session.clear()
        return RedirectResponse("/login?error=1", status_code=303)

    request.session.clear()
    request.session["authenticated"] = True
    return RedirectResponse("/dashboard", status_code=303)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse("/login", status_code=303)

    csrf_token = secrets.token_urlsafe(32)
    request.session["csrf_token"] = csrf_token

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"csrf_token": csrf_token},
    )


@router.post("/logout")
def logout(
    request: Request,
    csrf_token: str = Form(...),
):
    expected = request.session.get("csrf_token", "")
    if not expected or not secrets.compare_digest(csrf_token, expected):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    request.session.clear()
    return RedirectResponse("/login", status_code=303)


@router.get("/dashboard/data")
def dashboard_data(request: Request):
    if not request.session.get("authenticated"):
        raise HTTPException(status_code=401, detail="Login required")

    with sqlite3.connect("pijuice.db") as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM telemetry ORDER BY id DESC LIMIT 1"
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="No telemetry found")

    data = dict(row)
    payload = json.loads(data.get("payload_json") or "{}")
    system = payload.get("system") or {}
    battery_extended = payload.get("battery_extended") or {}
    leds = payload.get("leds") or {}

    return {
        "id": data["id"],
        "device_id": data["device_id"],
        "received_at": (
            data["received_at"].replace(" ", "T") + "Z"
            if data.get("received_at") else None
        ),
        "charge_percent": data["charge"],
        "battery_status": data["battery"],
        "power_input": data["power_input"],
        "voltage_mv": data["voltage"],
        "voltage_v": data["voltage"],
        "io_5v": data["io_5v"],
        "temperature_c": data["temperature"],
        "system": {
            "cpu_usage_percent": system.get("cpu_usage_percent"),
            "cpu_temperature_c": system.get("cpu_temperature_c"),
            "cpu_frequency_mhz": system.get("cpu_frequency_mhz"),
            "memory_total_mb": system.get("memory_total_mb"),
            "memory_available_mb": system.get("memory_available_mb"),
            "disk_total_gb": system.get("disk_total_gb"),
            "disk_free_gb": system.get("disk_free_gb"),
            "uptime_seconds": system.get("uptime_seconds"),
        },
        "leds": leds,
        "battery_extended": {
            "battery_current_ma": battery_extended.get("battery_current_ma"),
            "io_voltage_mv": battery_extended.get("io_voltage_mv"),
            "io_current_ma": battery_extended.get("io_current_ma"),
            "fault_status": battery_extended.get("fault_status"),
        },
    }


@router.get("/dashboard/history")
def dashboard_history(request: Request, hours: int = 1):
    if not request.session.get("authenticated"):
        raise HTTPException(status_code=401, detail="Login required")

    if hours not in (1, 6, 24):
        raise HTTPException(status_code=422, detail="hours must be 1, 6 or 24")

    with sqlite3.connect("pijuice.db") as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT received_at, charge, voltage, payload_json
            FROM telemetry
            WHERE received_at >= datetime('now', ?)
            ORDER BY received_at ASC
            LIMIT 2000
            """,
            (f"-{hours} hours",),
        ).fetchall()

    records = []
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        system = payload.get("system") or {}
        extended = payload.get("battery_extended") or {}

        total = system.get("memory_total_mb")
        available = system.get("memory_available_mb")
        memory_percent = (
            round((total - available) / total * 100, 1)
            if isinstance(total, (int, float))
            and isinstance(available, (int, float))
            and total > 0
            else None
        )

        records.append({
            "time": row["received_at"].replace(" ", "T") + "Z",
            "battery": row["charge"],
            "cpu_usage": system.get("cpu_usage_percent"),
            "cpu_temperature": system.get("cpu_temperature_c"),
            "memory_usage": memory_percent,
            "battery_voltage": row["voltage"],
            "battery_current": extended.get("battery_current_ma"),
            "io_voltage": (
                extended["io_voltage_mv"] / 1000
                if isinstance(extended.get("io_voltage_mv"), (int, float))
                else None
            ),
            "io_current": extended.get("io_current_ma"),
        })

    return {"hours": hours, "count": len(records), "records": records}
