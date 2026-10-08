import sqlite3

conn = sqlite3.connect("pijuice.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    received_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    device_id TEXT NOT NULL,
    charge INTEGER,
    battery TEXT,
    power_input TEXT,
    io_5v TEXT,
    voltage REAL,
    temperature REAL,
    temperature_status TEXT,
    fault INTEGER
)
""")

conn.commit()
conn.close()

print("Database initialized")
