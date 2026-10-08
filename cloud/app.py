import os
import sqlite3

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="PiJuice Cloud API")

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
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO telemetry (
                device_id, charge, battery, power_input, io_5v,
                voltage, temperature, temperature_status, fault
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            ),
        )
        telemetry_id = cursor.lastrowid

    return {"status": "stored", "id": telemetry_id}
