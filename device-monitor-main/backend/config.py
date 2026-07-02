"""
config.py

Central configuration for the Device Health Monitoring Platform.
Edit only this file when changing camera credentials or server settings.
"""

# ==========================================================
# CAMERA CONFIGURATION
# ==========================================================

CAMERA_IP = "10.45.0.2"
CAMERA_PORT = 8088

CAMERA_USERNAME = "admin"
CAMERA_PASSWORD = "admin123"

# ==========================================================
# DEVICE CONFIGURATION
# ==========================================================

DEVICE_ID = "CAM001"
DEVICE_TYPE = "AI_CAMERA"

# ==========================================================
# COLLECTOR CONFIGURATION
# ==========================================================

POLL_INTERVAL = 3  # seconds

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_NAME = "device_monitor.db"

# ==========================================================
# API CONFIGURATION
# ==========================================================

API_HOST = "127.0.0.1"
API_PORT = 8000

API_URL = f"http://{API_HOST}:{API_PORT}"

DEVICE_ENDPOINT = f"{API_URL}/device"
LATEST_ENDPOINT = f"{API_URL}/latest"
HISTORY_ENDPOINT = f"{API_URL}/history"
DEVICES_ENDPOINT = f"{API_URL}/devices"
ALERTS_ENDPOINT = f"{API_URL}/alerts"

# ==========================================================
# SUPABASE CONFIGURATION
# (Fill later)
# ==========================================================

SUPABASE_URL = ""
SUPABASE_KEY = ""

# ==========================================================
# DASHBOARD CONFIGURATION
# ==========================================================

DASHBOARD_REFRESH_SECONDS = 3

# ==========================================================
# LATENCY THRESHOLDS
# ==========================================================

LATENCY_GOOD = 50
LATENCY_WARNING = 100
LATENCY_CRITICAL = 150

# ==========================================================
# PACKET LOSS THRESHOLDS
# ==========================================================

PACKETLOSS_WARNING = 5
PACKETLOSS_CRITICAL = 15

# ==========================================================
# STREAM THRESHOLDS
# ==========================================================

MINIMUM_FPS = 20
MINIMUM_BITRATE = 1000

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

PROJECT_NAME = "Intelligent Device Health Monitoring Platform"

VERSION = "1.0.0"