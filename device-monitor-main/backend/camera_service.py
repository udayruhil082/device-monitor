"""
camera_service.py

Handles all communication with the ONVIF camera.

Responsibilities:
- Connect to camera
- Read device information
- Measure latency
- Read stream information
"""

import subprocess
import re
from onvif import ONVIFCamera

from config import (
    CAMERA_IP,
    CAMERA_PORT,
    CAMERA_USERNAME,
    CAMERA_PASSWORD,
)


class CameraService:

    def __init__(self):

        self.camera = None
        self.device_service = None
        self.media_service = None

    # ---------------------------------------------------
    # Connect to Camera
    # ---------------------------------------------------

    def connect(self):

        try:

            self.camera = ONVIFCamera(
                CAMERA_IP,
                CAMERA_PORT,
                CAMERA_USERNAME,
                CAMERA_PASSWORD,
            )

            self.device_service = self.camera.create_devicemgmt_service()
            self.media_service = self.camera.create_media_service()

            return True

        except Exception as e:

            print("Camera Connection Error:", e)

            return False

    # ---------------------------------------------------
    # Device Information
    # ---------------------------------------------------

    def get_device_information(self):

        try:

            info = self.device_service.GetDeviceInformation()

            return {

                "device_id": "CAM001",

                "device_type": "AI_CAMERA",

                "device_name": info.Model,

                "manufacturer": info.Manufacturer,

                "model": info.Model,

                "firmware": info.FirmwareVersion,

                "serial_number": info.SerialNumber,

                "hardware_id": getattr(info, "HardwareId", "N/A"),

                "ip_address": CAMERA_IP,

                "mac_address": "Not Available",

                "onvif_version": "2.0"

            }

        except Exception as e:

            print("Device Information Error:", e)

            return None

    # ---------------------------------------------------
    # Ping Latency
    # ---------------------------------------------------

    def get_latency(self):

        try:

            result = subprocess.run(
                ["ping", "-n", "1", CAMERA_IP],
                capture_output=True,
                text=True
            )

            match = re.search(r"time[=<](\d+)ms", result.stdout)

            if match:

                return int(match.group(1))

            return None

        except Exception:

            return None

    # ---------------------------------------------------
    # Stream Information
    # ---------------------------------------------------

    def get_stream_information(self):

        try:

            profiles = self.media_service.GetProfiles()

            profile = profiles[0]

            resolution = "Unknown"

            fps = "Unknown"

            bitrate = "Unknown"

            codec = "Unknown"

            try:

                encoder = profile.VideoEncoderConfiguration

                resolution = (
                    f"{encoder.Resolution.Width} x "
                    f"{encoder.Resolution.Height}"
                )

                fps = encoder.RateControl.FrameRateLimit

                bitrate = encoder.RateControl.BitrateLimit

                codec = str(encoder.Encoding)

            except Exception:
                pass

            return {

                "stream_status": "ONLINE",

                "resolution": resolution,

                "fps": fps,

                "bitrate": bitrate,

                "codec": codec

            }

        except Exception as e:

            print("Stream Information Error:", e)

            return {

                "stream_status": "OFFLINE",

                "resolution": "Not Available",

                "fps": "Not Available",

                "bitrate": "Not Available",

                "codec": "Not Available"

            }

       # ---------------------------------------------------
    # Live Metrics
    # ---------------------------------------------------

    def get_live_metrics(self):

        latency = self.get_latency()

        # Temporarily disable ONVIF stream lookup because it
        # causes long timeouts every loop.
        # We will enable it later after caching.
        # stream = self.get_stream_information()

        stream = {
            "stream_status": "ONLINE",
            "resolution": "Not Available",
            "fps": "Not Available",
            "bitrate": "Not Available",
            "codec": "Not Available"
        }

        return {

            "connection_status":
                "ONLINE" if latency is not None else "OFFLINE",

            "latency": latency if latency is not None else -1,

            "packet_loss": 0,

            "stream_status": stream["stream_status"],

            "resolution": stream["resolution"],

            "fps": stream["fps"],

            "bitrate": stream["bitrate"],

            "codec": stream["codec"]

        }