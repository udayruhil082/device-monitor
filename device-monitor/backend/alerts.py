from datetime import datetime

THRESHOLDS = {
    "battery_critical": 20,
    "battery_warning": 50,
    "latency_critical_ms": 200,
    "latency_warning_ms": 100,
    "temperature_critical_c": 85.0,
    "temperature_warning_c": 75.0,
    "cpu_critical_pct": 95.0,
    "cpu_warning_pct": 85.0,
}

alert_log = []

def evaluate_health(device, battery, latency_ms, connected, temperature=None, cpu_load=None):
    alerts = []
    timestamp = datetime.utcnow().isoformat()

    if not connected:
        alerts.append({
            "device": device,
            "level": "CRITICAL",
            "message": f"{device} is disconnected!",
            "timestamp": timestamp
        })

    if battery < THRESHOLDS["battery_critical"]:
        alerts.append({
            "device": device,
            "level": "CRITICAL",
            "message": f"{device} battery critically low: {battery}%",
            "timestamp": timestamp
        })
    elif battery < THRESHOLDS["battery_warning"]:
        alerts.append({
            "device": device,
            "level": "WARNING",
            "message": f"{device} battery low: {battery}%",
            "timestamp": timestamp
        })

    if latency_ms > THRESHOLDS["latency_critical_ms"]:
        alerts.append({
            "device": device,
            "level": "CRITICAL",
            "message": f"{device} latency critical: {latency_ms}ms",
            "timestamp": timestamp
        })
    elif latency_ms > THRESHOLDS["latency_warning_ms"]:
        alerts.append({
            "device": device,
            "level": "WARNING",
            "message": f"{device} latency high: {latency_ms}ms",
            "timestamp": timestamp
        })

    if temperature is not None:
        if temperature > THRESHOLDS["temperature_critical_c"]:
            alerts.append({
                "device": device,
                "level": "CRITICAL",
                "message": f"{device} temperature critically high: {temperature}°C!",
                "timestamp": timestamp
            })
        elif temperature > THRESHOLDS["temperature_warning_c"]:
            alerts.append({
                "device": device,
                "level": "WARNING",
                "message": f"{device} temperature high: {temperature}°C",
                "timestamp": timestamp
            })

    if cpu_load is not None:
        if cpu_load > THRESHOLDS["cpu_critical_pct"]:
            alerts.append({
                "device": device,
                "level": "CRITICAL",
                "message": f"{device} CPU load critically high: {cpu_load}%",
                "timestamp": timestamp
            })
        elif cpu_load > THRESHOLDS["cpu_warning_pct"]:
            alerts.append({
                "device": device,
                "level": "WARNING",
                "message": f"{device} CPU load high: {cpu_load}%",
                "timestamp": timestamp
            })

    alert_log.extend(alerts)
    return alerts

def get_all_alerts():
    return alert_log[-50:]