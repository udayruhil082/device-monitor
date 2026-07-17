"""
analytics.py

Calculates health analytics and predictive diagnostics.
"""

from database import db
from datetime import datetime


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
               # Predict Time To Failure
             # -------------------------------------------------

        prediction_minutes = None

        if len(history) >= 2:

         history_sorted = list(reversed(history))

        first = history_sorted[0]
        last = history_sorted[-1]
  
        t1 = datetime.fromisoformat(first["timestamp"])
        t2 = datetime.fromisoformat(last["timestamp"])

        elapsed_minutes = (t2 - t1).total_seconds() / 60

        if elapsed_minutes > 0:

         latency_growth = last["latency"] - first["latency"]

        growth_rate = latency_growth / elapsed_minutes

        CRITICAL_LATENCY = 150

        if growth_rate > 0:

            remaining = CRITICAL_LATENCY - last["latency"]

            if remaining > 0:

                prediction_minutes = remaining / growth_rate


        # -------------------------------------------------
        # AI Prediction
        # -------------------------------------------------

                # -------------------------------------------------
        # AI Prediction
        # -------------------------------------------------

        if prediction_minutes is None:

            prediction = "No failure predicted."

            diagnosis = (
                "Latency is stable."
            )

            recommendation = (
                "Continue monitoring."
            )

        elif prediction_minutes > 10:

            prediction = (
                f"Possible degradation in {prediction_minutes:.1f} minutes."
            )

            diagnosis = (
                "Latency is gradually increasing."
            )

            recommendation = (
                "Monitor network performance."
            )

        elif prediction_minutes > 5:

            prediction = (
                f"Failure expected in approximately {prediction_minutes:.1f} minutes."
            )

            diagnosis = (
                "Latency trend indicates growing congestion."
            )

            recommendation = (
                "Inspect the network before performance degrades."
            )

        elif prediction_minutes > 1:

            prediction = (
                f"Critical failure likely in {prediction_minutes:.1f} minutes."
            )

            diagnosis = (
                "Latency is rising rapidly."
            )

            recommendation = (
                "Immediate inspection recommended."
            )

        else:

            prediction = (
                "Failure expected within 1 minute."
            )

            diagnosis = (
                "Critical latency threshold is imminent."
            )

            recommendation = (
                "Immediate action required."
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