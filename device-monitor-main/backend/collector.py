"""
collector.py

Collects live telemetry from the AI Camera
and sends it to the FastAPI backend.
"""

import time
from datetime import datetime

import requests

from camera_service import CameraService
from config import (
    DEVICE_ENDPOINT,
    POLL_INTERVAL
)

camera = CameraService()


def main():

    print("=" * 60)
    print(" Intelligent Device Health Monitoring Platform ")
    print("=" * 60)

    if not camera.connect():
        print("❌ Unable to connect to camera.")
        return

    print("✅ Camera Connected Successfully")

    device_info = camera.get_device_information()

    if device_info is None:
        print("❌ Unable to read device information.")
        return

    while True:

        try:

            metrics = camera.get_live_metrics()

            payload = {
                "device": device_info,
                "metrics": {
                    "device_id": device_info["device_id"],
                    "connection_status": metrics["connection_status"],
                    "latency": metrics["latency"],
                    "packet_loss": metrics["packet_loss"],
                    "stream_status": metrics["stream_status"],
                    "resolution": metrics["resolution"],
                    "fps": metrics["fps"],
                    "bitrate": metrics["bitrate"],
                    "codec": metrics["codec"],
                    "timestamp": datetime.now().isoformat()
                }
            }

            response = requests.post(
                DEVICE_ENDPOINT,
                json=payload,
                timeout=5
            )

            if response.status_code == 200:

                print(
                    f"[{payload['metrics']['timestamp']}] "
                    f"{payload['metrics']['connection_status']} | "
                    f"Latency: {payload['metrics']['latency']} ms | "
                    f"FPS: {payload['metrics']['fps']} | "
                    f"Resolution: {payload['metrics']['resolution']}"
                )

            else:

                print(
                    "Backend Error:",
                    response.status_code,
                    response.text
                )

        except requests.exceptions.ConnectionError:

            print("❌ Backend is not running.")

        except Exception as e:

            print("Collector Error:", e)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()