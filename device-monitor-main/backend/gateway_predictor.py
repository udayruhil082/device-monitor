"""
gateway_predictor.py

Predicts gateway health and failure risk.
"""

from backend.gateway_analytics import analytics


class GatewayPredictor:

    def predict(self):

        analytics_data = analytics.get_analytics()

        score = analytics_data["health_score"]

        if score >= 90:

            risk = "LOW"

            probability = 5

            confidence = 98

            diagnosis = (
                "Gateway is operating normally. "
                "All monitored resources are healthy."
            )

            recommendation = (
                "No action required."
            )

        elif score >= 70:

            risk = "MEDIUM"

            probability = 35

            confidence = 92

            diagnosis = (
                "Gateway health is stable, "
                "but some resources require attention."
            )

            recommendation = (
                "Continue monitoring CPU, memory and network."
            )

        else:

            risk = "HIGH"

            probability = 85

            confidence = 95

            diagnosis = (
                "Gateway is likely to experience degraded "
                "performance if current conditions continue."
            )

            recommendation = (
                "Immediate investigation is recommended."
            )

        return {

            "risk": risk,

            "failure_probability": probability,

            "confidence": confidence,

            "diagnosis": diagnosis,

            "recommendation": recommendation

        }


predictor = GatewayPredictor()