from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from backend.database import save_reading, get_recent_readings
from backend.alerts import evaluate_health, get_all_alerts
from backend.predictor import predict_device_health

app = FastAPI()

class DeviceReading(BaseModel):
    device: str
    battery: float
    latency_ms: float
    connected: bool
    signal_strength: float = None
    cpu_load: float = None
    altitude_m: float = None
    temperature: float = None

@app.get("/")
def root():
    return {"status": "Device Health Monitor running"}

@app.post("/ingest")
def ingest(reading: DeviceReading):
    save_reading(
        device=reading.device,
        battery=reading.battery,
        latency_ms=reading.latency_ms,
        connected=reading.connected,
        temperature=reading.temperature,
        cpu_load=reading.cpu_load
    )
    alerts = evaluate_health(
        device=reading.device,
        battery=reading.battery,
        latency_ms=reading.latency_ms,
        connected=reading.connected,
        temperature=reading.temperature,
        cpu_load=reading.cpu_load
    )
    if alerts:
        print(f"ALERTS: {alerts}")
    return {
        "status": "ok",
        "received_at": datetime.utcnow().isoformat(),
        "alerts": alerts
    }

@app.get("/readings/{device_name}")
def get_readings(device_name: str):
    data = get_recent_readings(device_name)
    return {"device": device_name, "readings": data}

@app.get("/alerts")
def get_alerts():
    return {"alerts": get_all_alerts()}

@app.get("/predict/{device_name}")
def predict(device_name: str):
    return predict_device_health(device_name)