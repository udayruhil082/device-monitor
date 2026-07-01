import sqlite3
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "device_monitor.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS local_device_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device TEXT NOT NULL,
            battery REAL,
            latency_ms REAL,
            connected INTEGER,
            temperature REAL,
            cpu_load REAL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_reading(device, battery, latency_ms, connected, temperature=None, cpu_load=None):
    timestamp = datetime.utcnow().isoformat()
    # Save locally to SQLite
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO local_device_readings (device, battery, latency_ms, connected, temperature, cpu_load, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (device, battery, latency_ms, 1 if connected else 0, temperature, cpu_load, timestamp))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"SQLite save error: {e}")

    # Save to Supabase (only core fields)
    try:
        data = {
            "device": device,
            "battery": battery,
            "latency_ms": latency_ms,
            "connected": connected
        }
        supabase.table("device_readings").insert(data).execute()
    except Exception as e:
        print(f"Supabase save error (non-blocking): {e}")

def get_recent_readings(device_name, limit=30):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT battery, latency_ms, connected, temperature, cpu_load, timestamp 
            FROM local_device_readings
            WHERE device = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (device_name, limit))
        rows = cursor.fetchall()
        conn.close()
        
        readings = []
        for r in rows:
            readings.append({
                "battery": r["battery"],
                "latency_ms": r["latency_ms"],
                "connected": bool(r["connected"]),
                "temperature": r["temperature"],
                "cpu_load": r["cpu_load"],
                "timestamp": r["timestamp"]
            })
        return readings
    except Exception as e:
        print(f"SQLite read error: {e}")
        return []