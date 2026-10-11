import os
import sqlite3

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="PiJuice Cloud API")

# Dashboard session and authentication routes
from starlette.middleware.sessions import SessionMiddleware
from dashboard_routes import router as dashboard_router

_session_secret = os.environ.get("DASHBOARD_SESSION_SECRET", "")
if len(_session_secret) < 32:
    raise RuntimeError("DASHBOARD_SESSION_SECRET is missing or too short")

app.add_middleware(
    SessionMiddleware,
    secret_key=_session_secret,
    session_cookie="pijuice_dashboard",
    max_age=60 * 60 * 8,
    same_site="lax",
    https_only=True,
)
app.include_router(dashboard_router)


DB_PATH = "pijuice.db"
API_TOKEN = os.environ.get("PIJUICE_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("PIJUICE_API_TOKEN is not configured")

class Telemetry(BaseModel):
    device_id: str
    charge: int | None = None
    battery: str | None = None
    power_input: str | None = None
    io_5v: str | None = None
    voltage: float | None = None
    temperature: float | None = None
    temperature_status: str | None = None
    fault: bool | None = None
    schema_version: int | None = None
    payload_json: dict | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/telemetry")
def receive_telemetry(
    data: Telemetry,
    x_api_token: str | None = Header(default=None),
):
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
    payload_text = None
    if data.payload_json is not None:
        import json
        payload_text = json.dumps(
            data.payload_json,
            ensure_ascii=False,
            separators=(",", ":")
        )
        if len(payload_text.encode("utf-8")) > 65536:
            raise HTTPException(
                status_code=413,
                detail="Telemetry payload too large"
            )

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO telemetry (
                device_id, charge, battery, power_input, io_5v,
                voltage, temperature, temperature_status, fault,
                schema_version, payload_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.device_id,
                data.charge,
                data.battery,
                data.power_input,
                data.io_5v,
                data.voltage,
                data.temperature,
                data.temperature_status,
                data.fault,
                data.schema_version,
                payload_text,
            ),
        )
        telemetry_id = cursor.lastrowid

    return {"status": "stored", "id": telemetry_id}


@app.get("/api/telemetry/latest")
def get_latest_telemetry(
    x_api_token: str | None = Header(default=None),
):
    import json

    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT *
            FROM telemetry
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="No telemetry found")

    result = dict(row)

    if result["payload_json"]:
        result["payload_json"] = json.loads(result["payload_json"])

    return result


@app.get("/api/telemetry/history")
def get_telemetry_history(
    limit: int = 100,
    x_api_token: str | None = Header(default=None),
):
    import json

    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")

    if not 1 <= limit <= 1000:
        raise HTTPException(
            status_code=422,
            detail="limit must be between 1 and 1000"
        )

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT *
            FROM telemetry
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    results = []
    for row in reversed(rows):
        record = dict(row)
        if record["payload_json"]:
            record["payload_json"] = json.loads(record["payload_json"])
        results.append(record)

    return {
        "count": len(results),
        "records": results,
    }
