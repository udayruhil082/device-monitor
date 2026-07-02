"""
analytics.py

Calculates health analytics and predictive diagnostics.
"""

from database import db


class AnalyticsService:

    # ==========================================================
    # Get Analytics
    # ==========================================================

    def get_analytics(self, device_id):

        history = db.history(100)

        history = [
            h for h in history
            if h["device_id"] == device_id
        ]

        if len(history) == 0:

            return {

                "device_id": device_id,

                "average_latency": 0,

                "maximum_latency": 0,

                "minimum_latency": 0,

                "connection_stability": 0,

                "downtime": 0,

                "health_score": 0,

                "prediction": "No Data",

                "recommendation": "No recommendation available.",

                "failure_risk": "UNKNOWN",

                "diagnosis": "No telemetry received from device."

            }

        # -------------------------------------------------
        # Latency Statistics
        # -------------------------------------------------

        latencies = [

            h["latency"]

            for h in history

            if h["latency"] >= 0

        ]

        avg_latency = (

            sum(latencies) / len(latencies)

            if latencies else 0

        )

        max_latency = max(latencies) if latencies else 0

        min_latency = min(latencies) if latencies else 0

        # -------------------------------------------------
        # Connection Statistics
        # -------------------------------------------------

        online = len(

            [

                h for h in history

                if h["connection_status"] == "ONLINE"

            ]

        )

        stability = round(

            (online / len(history)) * 100,

            2

        )

        downtime = round(

            100 - stability,

            2

        )

        # -------------------------------------------------
        # Health Score
        # -------------------------------------------------

        health = 100

        # Latency penalties

        if avg_latency > 40:
            health -= 5

        if avg_latency > 60:
            health -= 10

        if avg_latency > 100:
            health -= 20

        if avg_latency > 150:
            health -= 30

        # Stability penalties

        if stability < 98:
            health -= 5

        if stability < 95:
            health -= 10

        if stability < 90:
            health -= 15

        if stability < 80:
            health -= 20

        health = max(0, min(100, health))

        # -------------------------------------------------
        # Failure Risk
        # -------------------------------------------------

        if avg_latency < 60 and stability >= 98:

            failure_risk = "LOW"

        elif avg_latency <= 100:

            failure_risk = "MEDIUM"

        else:

            failure_risk = "HIGH"

        # -------------------------------------------------
        # AI Prediction
        # -------------------------------------------------

        if failure_risk == "LOW":

            prediction = "No Failure Expected"

            diagnosis = (
                "System is healthy. "
                "No abnormal behaviour detected."
            )

            recommendation = (
                "Continue normal monitoring."
            )

        elif failure_risk == "MEDIUM":

            prediction = (
                "Network Degradation Expected"
            )

            diagnosis = (
                "Increasing latency trend detected. "
                "Possible network congestion."
            )

            recommendation = (
                "Inspect network connection and continue monitoring."
            )

        else:

            prediction = (
                "Possible Device Failure"
            )

            diagnosis = (
                "Critical latency detected. "
                "Camera may disconnect if conditions persist."
            )

            recommendation = (
                "Immediate inspection recommended. "
                "Check network connectivity and restart the camera if required."
            )

        return {

            "device_id": device_id,

            "average_latency": round(avg_latency, 2),

            "maximum_latency": max_latency,

            "minimum_latency": min_latency,

            "connection_stability": stability,

            "downtime": downtime,

            "health_score": health,

            "prediction": prediction,

            "recommendation": recommendation,

            "failure_risk": failure_risk,

            "diagnosis": diagnosis

        }


analytics = AnalyticsService()