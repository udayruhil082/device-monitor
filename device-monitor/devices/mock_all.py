import requests
import time
import random

BACKEND = "http://127.0.0.1:8000/ingest"

devices = {
    "AI Camera": {"battery": 85.0, "latency": 80.0,  "connected": True},
    "Drone":     {"battery": 70.0, "latency": 60.0,  "connected": True},
}

print("Simulating AI Camera + Drone — sending data every 10 seconds...")

while True:
    for name, d in devices.items():
        # Reset battery when hits 0 (like recharging)
        if d["battery"] <= 0:
            d["battery"] = 85.0
            print(f"🔋 {name} recharged!")

        # Reset latency if goes too high
        if d["latency"] > 300:
            d["latency"] = 60.0

        d["battery"]   = max(0,  d["battery"] + random.uniform(-1, 0.1))
        d["latency"]   = max(10, d["latency"] + random.uniform(-5, 8))
        d["connected"] = random.random() > 0.05

        payload = {
            "device":     name,
            "battery":    round(d["battery"], 1),
            "latency_ms": round(d["latency"], 1),
            "connected":  d["connected"]
        }

        try:
            requests.post(BACKEND, json=payload, timeout=5)
            print(f"✅ {name}: battery={payload['battery']}% latency={payload['latency_ms']}ms")
        except Exception as e:
            print(f"❌ {name}: {e}")

    print("--- 10 seconds ---\n")
    time.sleep(10)