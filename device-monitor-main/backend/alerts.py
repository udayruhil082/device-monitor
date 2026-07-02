"""
alerts.py

Generates intelligent real-time alerts from live device telemetry.
"""

from datetime import datetime


class AlertService:

    def __init__(self):
        self.active_alerts = []

    # ==========================================================
    # Generate Alerts
    # ==========================================================

    def evaluate(self, metrics):

        alerts = []

        latency = metrics["latency"]
        packet_loss = metrics["packet_loss"]
        connection = metrics["connection_status"]

        current_time = datetime.now().strftime("%I:%M %p")

        # -------------------------------------------------
        # Camera Connection
        # -------------------------------------------------

        if connection != "ONLINE":

            alerts.append({

                "time": current_time,

                "level": "CRITICAL",

                "title": "Camera Offline",

                "message": "Camera is unreachable. Device monitoring has stopped."

            })

        # -------------------------------------------------
        # Latency Alerts
        # -------------------------------------------------

        elif latency > 100:

            alerts.append({

                "time": current_time,

                "level": "CRITICAL",

                "title": "Critical Latency",

                "message": f"Latency reached {latency} ms. Device failure risk is HIGH."

            })

        elif latency >= 60:

            alerts.append({

                "time": current_time,

                "level": "WARNING",

                "title": "Latency Warning",

                "message": f"Latency increased to {latency} ms."

            })

        # -------------------------------------------------
        # Packet Loss
        # -------------------------------------------------

        if packet_loss >= 5:

            alerts.append({

                "time": current_time,

                "level": "WARNING",

                "title": "Packet Loss Detected",

                "message": f"Packet loss reached {packet_loss}%."

            })

        # -------------------------------------------------
        # Healthy Status
        # -------------------------------------------------

        if (
            connection == "ONLINE"
            and latency < 60
            and packet_loss < 5
        ):

            alerts.append({

                "time": current_time,

                "level": "INFO",

                "title": "Device Healthy",

                "message": "Camera operating normally."

            })

        self.active_alerts = alerts

        return alerts

    # ==========================================================
    # Current Alerts
    # ==========================================================

    def get_alerts(self):

        return self.active_alerts


alerts = AlertService()