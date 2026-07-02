"""
main.py

Intelligent Device Health Monitoring Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db
from analytics import analytics
from alerts import alerts

app = FastAPI(
    title="Intelligent Device Health Monitoring Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return {
        "project": "Intelligent Device Health Monitoring Platform",
        "status": "Running"
    }


# =====================================================
# RECEIVE DEVICE TELEMETRY
# =====================================================

@app.post("/device")
def receive_device(payload: dict):

    try:

        device = payload["device"]
        metrics = payload["metrics"]

        # Save static device information
        db.save_device(device)

        # Save live metrics
        db.save_metrics(metrics)

        # Generate alerts
        generated_alerts = alerts.evaluate(metrics)

        # Generate analytics
        generated_analytics = analytics.get_analytics(
            device["device_id"]
        )

        return {

            "success": True,

            "message": "Telemetry Stored Successfully.",

            "alerts": generated_alerts,

            "analytics": generated_analytics

        }

    except Exception as e:

        return {

            "success": False,

            "message": str(e)

        }


# =====================================================
# LATEST COMPLETE DATA
# =====================================================

@app.get("/latest")
def latest():

    latest_metrics = db.latest_metrics()

    if latest_metrics is None:

        return {

            "success": False,

            "message": "No telemetry available."

        }

    device = db.get_device(
        latest_metrics["device_id"]
    )

    analytics_data = analytics.get_analytics(
        latest_metrics["device_id"]
    )

    active_alerts = alerts.get_alerts()

    return {

        "success": True,

        "device": device,

        "metrics": latest_metrics,

        "analytics": analytics_data,

        "alerts": active_alerts

    }


# =====================================================
# HISTORY
# =====================================================

@app.get("/history")
def history(limit: int = 50):

    return {

        "success": True,

        "history": db.history(limit)

    }


# =====================================================
# DEVICE LIST
# =====================================================

@app.get("/devices")
def devices():

    return {

        "success": True,

        "devices": db.get_devices()

    }


# =====================================================
# SINGLE DEVICE
# =====================================================

@app.get("/device/{device_id}")
def device(device_id: str):

    device = db.get_device(device_id)

    if device is None:

        return {

            "success": False,

            "message": "Device Not Found"

        }

    analytics_data = analytics.get_analytics(device_id)

    history = [

        item for item in db.history(100)

        if item["device_id"] == device_id

    ]

    return {

        "success": True,

        "device": device,

        "analytics": analytics_data,

        "history": history

    }


# =====================================================
# ANALYTICS
# =====================================================

@app.get("/analytics/{device_id}")
def analytics_endpoint(device_id: str):

    return {

        "success": True,

        "analytics": analytics.get_analytics(device_id)

    }


# =====================================================
# ALERTS
# =====================================================

@app.get("/alerts")
def alerts_endpoint():

    return {

        "success": True,

        "alerts": alerts.get_alerts()

    }


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health():

    latest = db.latest_metrics()

    if latest is None:

        return {

            "status": "No Data"

        }

    return {

        "status": latest["connection_status"],

        "latency": latest["latency"]

    }