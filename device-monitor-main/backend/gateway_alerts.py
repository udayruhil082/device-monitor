"""
gateway_alerts.py

Generates intelligent alerts for the IoT Gateway.
"""

from backend.gateway_analytics import analytics


class GatewayAlerts:

    def get_alerts(self):

        analytics_data = analytics.get_analytics()

        data = analytics_data["live"]

        score = analytics_data["health_score"]

        cpu = data["cpu"]["usage"]

        memory = data["memory"]["usage_percent"]

        alerts = []

        # ==========================================
        # HEALTHY (GREEN)
        # ==========================================

        if score >= 75:

            alerts.append({

                "severity": "LOW",

                "title": "Gateway Operating Normally",

                "message":
                "All monitored gateway resources are operating within normal limits.",

                "impact":
                "No performance or connectivity issues have been detected.",

                "action":
                "No action required. Continue routine monitoring."

            })

        # ==========================================
        # WARNING (YELLOW)
        # ==========================================

        elif score >= 60:

            reasons = []

            if cpu >= 75:
                reasons.append(f"CPU utilization is {cpu}%.")

            if memory >= 75:
                reasons.append(f"Memory utilization is {memory}%.")

            if not reasons:
                reasons.append(
                    f"Gateway Health Score is {score}/100, indicating preventive monitoring is recommended."
                )

            alerts.append({

                "severity": "MEDIUM",

                "title": "Gateway Performance Monitoring Recommended",

                "message":
                " ".join(reasons),

                "impact":
                "The gateway is operating normally, but continued monitoring is recommended to prevent future issues.",

                "action":
                "Continue monitoring CPU, memory and network performance."

            })

        # ==========================================
        # CRITICAL (RED)
        # ==========================================

        else:

            reasons = []

            if cpu >= 90:
                reasons.append(f"Critical CPU utilization detected ({cpu}%).")

            if memory >= 90:
                reasons.append(f"Critical memory utilization detected ({memory}%).")

            if not reasons:
                reasons.append(
                    f"Gateway Health Score has dropped to {score}/100."
                )

            alerts.append({

                "severity": "HIGH",

                "title": "Gateway Health Critical",

                "message":
                " ".join(reasons),

                "impact":
                "There is a high probability of degraded gateway performance or service interruption.",

                "action":
                "Immediate investigation and corrective action are recommended."

            })

        return alerts


alerts = GatewayAlerts()