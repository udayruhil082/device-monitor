from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from backend.database import save_reading, get_recent_readings

app = FastAPI()

class DeviceReading(BaseModel):
    device: str
    battery: float
    latency_ms: float
    connected: bool
    signal_strength: float = None
    cpu_load: float = None
    altitude_m: float = None

@app.get("/")
def root():
    return {"status": "Device Health Monitor running"}

@app.post("/ingest")
def ingest(reading: DeviceReading):
    save_reading(
        device=reading.device,
        battery=reading.battery,
        latency_ms=reading.latency_ms,
        connected=reading.connected
    )
    print(f"[{datetime.utcnow()}] Saved: {reading.device} battery={reading.battery}%")
    return {"status": "ok", "received_at": datetime.utcnow().isoformat()}

@app.get("/readings/{device_name}")
def get_readings(device_name: str):
    data = get_recent_readings(device_name)
    return {"device": device_name, "readings": data}