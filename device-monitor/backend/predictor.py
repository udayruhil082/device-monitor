import numpy as np
from backend.database import get_recent_readings

def predict_device_health(device_name):
    readings = get_recent_readings(device_name, limit=20)

    if len(readings) < 3:
        return {
            "device": device_name,
            "status": "COLLECTING DATA",
            "message": f"Need more readings — only {len(readings)} so far, need at least 3",
            "health_score": None,
            "battery_health": None,
            "time_to_die_mins": None,
            "latency_trend": None,
            "connection_stability": None,
        }

    readings = list(reversed(readings))
    batteries   = [r["battery"] for r in readings]
    latencies   = [r["latency_ms"] for r in readings]
    connections = [1 if r["connected"] else 0 for r in readings]
    x = np.arange(len(readings))

    battery_slope, _  = np.polyfit(x, batteries, 1)
    drain_per_minute  = battery_slope * 6

    current_battery = batteries[-1]
    if drain_per_minute < 0:
        time_to_die_mins = round(current_battery / abs(drain_per_minute), 1)
    else:
        time_to_die_mins = None

    drain_rate_abs = abs(battery_slope)
    if drain_rate_abs < 0.1:
        battery_health = 100
    elif drain_rate_abs < 0.3:
        battery_health = 85
    elif drain_rate_abs < 0.6:
        battery_health = 70
    elif drain_rate_abs < 1.0:
        battery_health = 50
    else:
        battery_health = 30

    latency_slope, _ = np.polyfit(x, latencies, 1)
    if latency_slope > 5:
        latency_trend = "RISING FAST — disconnection risk"
    elif latency_slope > 1:
        latency_trend = "slowly increasing"
    elif latency_slope < -1:
        latency_trend = "improving"
    else:
        latency_trend = "stable"

    stability = round(sum(connections) / len(connections) * 100, 1)

    score  = min(current_battery, 100) * 0.35
    score += battery_health * 0.25
    score += stability * 0.25
    score += max(0, 100 - latencies[-1] / 3) * 0.15
    health_score = round(score, 1)

    if health_score >= 75:
        status = "HEALTHY"
    elif health_score >= 50:
        status = "AT RISK"
    else:
        status = "CRITICAL — failure predicted"

    if time_to_die_mins and time_to_die_mins < 10:
        message = f"⚠️ Battery will die in ~{time_to_die_mins} mins at current drain rate"
    elif time_to_die_mins:
        message = f"Battery will last ~{time_to_die_mins} more minutes"
    else:
        message = "Battery stable — no drain detected"

    return {
        "device": device_name,
        "status": status,
        "health_score": health_score,
        "battery_health": battery_health,
        "current_battery": current_battery,
        "time_to_die_mins": time_to_die_mins,
        "drain_per_minute": round(drain_per_minute, 3),
        "latency_trend": latency_trend,
        "current_latency_ms": latencies[-1],
        "connection_stability": stability,
        "readings_used": len(readings),
        "message": message
    }