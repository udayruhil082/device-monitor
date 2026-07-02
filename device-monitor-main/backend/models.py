"""
models.py

Pydantic models used across the backend.
"""

from pydantic import BaseModel
from typing import Optional


# ==========================================================
# DEVICE INFORMATION
# ==========================================================

class DeviceInformation(BaseModel):

    device_id: str
    device_type: str

    device_name: str
    manufacturer: str
    model: str

    firmware: str

    serial_number: str
    hardware_id: str

    ip_address: str
    mac_address: str

    onvif_version: str


# ==========================================================
# LIVE METRICS
# ==========================================================

class LiveMetrics(BaseModel):

    device_id: str

    connection_status: str

    latency: int

    packet_loss: float

    stream_status: str

    resolution: str

    fps: Optional[int | str]

    bitrate: Optional[int | str]

    codec: str

    timestamp: str


# ==========================================================
# COMPLETE DEVICE PAYLOAD
# ==========================================================

class DevicePayload(BaseModel):

    device: DeviceInformation

    metrics: LiveMetrics


# ==========================================================
# ALERT
# ==========================================================

class Alert(BaseModel):

    device_id: str

    level: str

    title: str

    message: str

    timestamp: str

    resolved: bool = False


# ==========================================================
# ANALYTICS
# ==========================================================

class Analytics(BaseModel):

    device_id: str

    average_latency: float

    maximum_latency: float

    minimum_latency: float

    connection_stability: float

    downtime: float

    health_score: float

    prediction: str

    recommendation: str


# ==========================================================
# SETTINGS
# ==========================================================

class DeviceSettings(BaseModel):

    ip_address: str

    username: str

    password: str

    polling_interval: int


# ==========================================================
# API RESPONSE
# ==========================================================

class ApiResponse(BaseModel):

    success: bool

    message: str

    data: Optional[dict] = None