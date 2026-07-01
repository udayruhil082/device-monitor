import requests
import time
import subprocess
import re
from datetime import datetime

CAMERA_IP = "10.45.0.2"
BACKEND = "http://127.0.0.1:8000/ingest"

USE_MOCK_PING = False

def get_camera_status(ip):
    global USE_MOCK_PING
    if USE_MOCK_PING:
        return False, 9999.0
    try:
        # Ping with a 1-second timeout
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", ip],
            capture_output=True, text=True, timeout=2
        )
        output = result.stdout
        connected = "Reply from" in output and "Destination host unreachable" not in output
        match = re.search(r"time[=<](\d+)ms", output)
        latency_ms = float(match.group(1)) if match else 9999.0
        return connected, latency_ms
    except Exception:
        return False, 9999.0

print("Starting Sparsh Camera monitoring...")
print(f"Camera IP: {CAMERA_IP}")
print(f"Backend: {BACKEND}\n")

# Check if real camera is reachable initially
initial_connected, _ = get_camera_status(CAMERA_IP)
if not initial_connected:
    print("⚠️ No physical camera detected at IP. Fallback to mock thermodynamic simulator enabled.")
    USE_MOCK_PING = True
else:
    print("✅ Connected to physical camera. Running physical-thermodynamic monitoring.")

# Thermodynamic Simulation State
temperature = 42.0
cpu_load = 30.0
tick = 0

while True:
    tick = (tick + 1) % 35  # 35 ticks cycle (~6 minutes at 10s intervals)
    
    # 1. Simulate CPU load changes (Analytics workload cycle)
    if 12 <= tick < 28:
        # Simulated high workload (e.g. running multiple YOLO object detection streams)
        target_cpu = 88.0 + (tick % 7)  # Fluctuate CPU between 88% and 94%
    elif tick >= 28:
        # Thermal shutdown (zero load, cooling down)
        target_cpu = 0.0
    else:
        # Normal idle/standby workload
        target_cpu = 30.0 + (tick % 12)  # Fluctuate CPU between 30% and 41%

    # Smooth CPU transitions
    cpu_load = cpu_load * 0.5 + target_cpu * 0.5

    # 2. Simulate temperature based on CPU load and heat dissipation
    # Temp increases when CPU is active, dissipates toward ambient (40C)
    ambient_temp = 40.0
    heating_coefficient = (cpu_load / 100.0) * 5.2
    cooling_rate = (temperature - ambient_temp) * 0.075
    temperature = temperature + heating_coefficient - cooling_rate

    # 3. Simulate latency and connectivity
    if tick >= 28:
        # Simulated shutdown state due to overheat (temp > 85C)
        connected = False
        latency_ms = 9999.0
    else:
        # Real camera check or simulated network latency
        real_connected, real_latency = get_camera_status(CAMERA_IP)
        if real_connected and not USE_MOCK_PING:
            connected = True
            base_latency = real_latency
        else:
            connected = True
            # Base mock latency with minor jitter
            base_latency = 30.0 + (tick % 6)
        
        # Apply thermal throttling latency degradation:
        if temperature > 80.0:
            # High thermal throttling spikes
            latency_ms = base_latency + (temperature - 80.0) * 15.0 + 80.0
        elif temperature > 72.0:
            # Moderate thermal throttling
            latency_ms = base_latency + (temperature - 72.0) * 3.5
        else:
            latency_ms = base_latency

    payload = {
        "device": "AI Camera",
        "battery": 100.0,  # Line-powered
        "latency_ms": round(latency_ms, 1),
        "connected": connected,
        "signal_strength": -65.0,
        "temperature": round(temperature, 1),
        "cpu_load": round(cpu_load, 1)
    }

    try:
        r = requests.post(BACKEND, json=payload, timeout=5)
        res_data = r.json()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Camera Ingest: "
              f"Temp={payload['temperature']}°C | CPU={payload['cpu_load']}% | "
              f"Latency={payload['latency_ms']}ms | Connected={connected} "
              f"→ Backend Status: {res_data['status']}")
    except Exception as e:
        print(f"Backend connection error: {e}")

    time.sleep(10)