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
            "current_temp": None,
            "temp_health": None,
            "temp_trend": None,
            "time_to_overheat_mins": None,
            "current_cpu_load": None,
            "cpu_trend": None,
            "time_to_latency_spike_mins": None,
        }

    readings = list(reversed(readings))
    batteries    = [r["battery"] for r in readings]
    latencies    = [r["latency_ms"] for r in readings]
    connections  = [1 if r["connected"] else 0 for r in readings]
    temperatures = [r.get("temperature") for r in readings]
    cpu_loads    = [r.get("cpu_load") for r in readings]
    x = np.arange(len(readings))

    battery_slope, _  = np.polyfit(x, batteries, 1)
    drain_per_minute  = battery_slope * 6

    current_battery = batteries[-1]
    if drain_per_minute < -0.05:
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

    # Latency slope & forecasting
    latency_slope, _ = np.polyfit(x, latencies, 1)
    latency_rise_per_minute = latency_slope * 6
    if latency_slope > 5:
        latency_trend = "RISING FAST — disconnection risk"
    elif latency_slope > 1:
        latency_trend = "slowly increasing"
    elif latency_slope < -1:
        latency_trend = "improving"
    else:
        latency_trend = "stable"

    current_latency = latencies[-1]
    if latency_rise_per_minute > 0.5:
        time_to_latency_spike = (200.0 - current_latency) / latency_rise_per_minute
        time_to_latency_spike_mins = max(0.0, round(time_to_latency_spike, 1))
    else:
        time_to_latency_spike_mins = None

    stability = round(sum(connections) / len(connections) * 100, 1)

    # Temperature & CPU load analysis
    current_temp = temperatures[-1] if temperatures and temperatures[-1] is not None else None
    current_cpu = cpu_loads[-1] if cpu_loads and cpu_loads[-1] is not None else None

    temp_trend = "stable"
    time_to_overheat_mins = None
    temp_health = 100.0

    if current_temp is not None:
        # Calculate temperature health
        if current_temp <= 60.0:
            temp_health = 100.0
        elif current_temp >= 85.0:
            temp_health = 0.0
        else:
            temp_health = max(0.0, round(100.0 - (current_temp - 60.0) * 4, 1))

        # Temperature forecasting
        valid_temp_indices = [i for i, t in enumerate(temperatures) if t is not None]
        if len(valid_temp_indices) >= 3:
            x_temp = np.array(valid_temp_indices)
            y_temp = np.array([temperatures[i] for i in valid_temp_indices])
            temp_slope, _ = np.polyfit(x_temp, y_temp, 1)
            temp_rise_per_minute = temp_slope * 6

            if temp_rise_per_minute > 1.5:
                temp_trend = "RISING FAST — overheating risk"
            elif temp_rise_per_minute > 0.5:
                temp_trend = "slowly increasing"
            elif temp_rise_per_minute < -0.5:
                temp_trend = "decreasing"
            else:
                temp_trend = "stable"

            if temp_rise_per_minute > 0.05:
                time_to_overheat = (85.0 - current_temp) / temp_rise_per_minute
                time_to_overheat_mins = max(0.0, round(time_to_overheat, 1))

    cpu_trend = "stable"
    cpu_health = 100.0
    if current_cpu is not None:
        cpu_health = max(0.0, round(100.0 - current_cpu, 1))
        valid_cpu_indices = [i for i, c in enumerate(cpu_loads) if c is not None]
        if len(valid_cpu_indices) >= 3:
            x_cpu = np.array(valid_cpu_indices)
            y_cpu = np.array([cpu_loads[i] for i in valid_cpu_indices])
            cpu_slope, _ = np.polyfit(x_cpu, y_cpu, 1)
            cpu_change_per_minute = cpu_slope * 6
            if cpu_change_per_minute > 2.0:
                cpu_trend = "rising"
            elif cpu_change_per_minute < -2.0:
                cpu_trend = "falling"
            else:
                cpu_trend = "stable"

    # Calculate overall health score
    if current_temp is not None:
        # Thermal-aware health score
        # Weights: Battery 20%, Stability 25%, Latency 15%, Temp Health 25%, CPU Health 15%
        score  = min(current_battery, 100) * 0.20
        score += stability * 0.25
        score += max(0.0, 100.0 - latencies[-1] / 3) * 0.15
        score += temp_health * 0.25
        score += cpu_health * 0.15
        health_score = round(score, 1)
    else:
        # Standard battery-centric health score
        score  = min(current_battery, 100) * 0.35
        score += battery_health * 0.25
        score += stability * 0.25
        score += max(0.0, 100.0 - latencies[-1] / 3) * 0.15
        health_score = round(score, 1)

    # Set status
    if health_score >= 75:
        status = "HEALTHY"
    elif health_score >= 50:
        status = "AT RISK"
    else:
        status = "CRITICAL — failure predicted"

    # Override status if imminent failure
    if (time_to_overheat_mins is not None and time_to_overheat_mins < 5.0) or \
       (time_to_latency_spike_mins is not None and time_to_latency_spike_mins < 5.0) or \
       (time_to_die_mins is not None and time_to_die_mins < 5.0):
        status = "CRITICAL — failure predicted"

    # Construct prediction message
    messages = []
    if time_to_overheat_mins is not None:
        if time_to_overheat_mins < 5.0:
            messages.append(f"🚨 Camera overheating: failure predicted in ~{time_to_overheat_mins} mins!")
        else:
            messages.append(f"Camera temperature rising: overheat expected in ~{time_to_overheat_mins} mins.")

    if time_to_latency_spike_mins is not None:
        if time_to_latency_spike_mins < 5.0:
            messages.append(f"⚠️ High connection latency spike expected in ~{time_to_latency_spike_mins} mins!")
        else:
            messages.append(f"Connection latency is rising: spike expected in ~{time_to_latency_spike_mins} mins.")

    if time_to_die_mins is not None:
        if time_to_die_mins < 10.0:
            messages.append(f"⚠️ Battery will die in ~{time_to_die_mins} mins at current drain.")
        else:
            messages.append(f"Battery will last ~{time_to_die_mins} more mins.")

    if not messages:
        if current_temp is not None:
            messages.append("All metrics stable — no immediate failure risk detected.")
        else:
            messages.append("Battery stable — no drain detected.")

    message = " | ".join(messages)

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
        "message": message,
        
        # New fields
        "current_temp": current_temp,
        "temp_health": temp_health,
        "temp_trend": temp_trend,
        "time_to_overheat_mins": time_to_overheat_mins,
        "current_cpu_load": current_cpu,
        "cpu_trend": cpu_trend,
        "time_to_latency_spike_mins": time_to_latency_spike_mins,
    }