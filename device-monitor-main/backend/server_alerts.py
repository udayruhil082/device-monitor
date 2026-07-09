from backend.server_analytics import analytics
from backend.server_predictor import predictor


class ServerAlerts:

    def __init__(self):
        pass

    # ==========================================
    # Generate Alerts
    # ==========================================

    def get_alerts(self):

        data = analytics.get_analytics()

        avg = data["averages"]

        health = data["health_score"]

        prediction = predictor.predict()

        alerts = []

        # ======================================
        # CPU
        # ======================================

        if avg["cpu"] >= 95:

            alerts.append({

                "level": "CRITICAL",

                "title": "CPU Critical",

                "message": "Average CPU utilization is above 95%."

            })

        elif avg["cpu"] >= 80:

            alerts.append({

                "level": "WARNING",

                "title": "High CPU",

                "message": "Average CPU utilization is above 80%."

            })

        # ======================================
        # RAM
        # ======================================

        if avg["ram"] >= 95:

            alerts.append({

                "level": "CRITICAL",

                "title": "Memory Critical",

                "message": "Average RAM utilization is above 95%."

            })

        elif avg["ram"] >= 80:

            alerts.append({

                "level": "WARNING",

                "title": "High Memory",

                "message": "Average RAM utilization is above 80%."

            })

        # ======================================
        # Disk
        # ======================================

        if avg["disk"] >= 95:

            alerts.append({

                "level": "CRITICAL",

                "title": "Disk Critical",

                "message": "Disk storage is almost full."

            })

        elif avg["disk"] >= 85:

            alerts.append({

                "level": "WARNING",

                "title": "Disk Warning",

                "message": "Disk usage is increasing."

            })

        # ======================================
        # Load Average
        # ======================================

        if avg["load"] >= 8:

            alerts.append({

                "level": "CRITICAL",

                "title": "High Load",

                "message": "Server load average is critically high."

            })

        elif avg["load"] >= 5:

            alerts.append({

                "level": "WARNING",

                "title": "Load Warning",

                "message": "Server load is above the recommended limit."

            })

        # ======================================
        # Health Score
        # ======================================

        if health <= 50:

            alerts.append({

                "level": "CRITICAL",

                "title": "Health Critical",

                "message": "Overall server health is critical."

            })

        elif health <= 70:

            alerts.append({

                "level": "WARNING",

                "title": "Health Warning",

                "message": "Server health is degrading."

            })

        # ======================================
        # Failure Probability
        # ======================================

        if prediction["failure_probability"] >= 80:

            alerts.append({

                "level": "CRITICAL",

                "title": "Failure Risk",

                "message": "High probability of server failure."

            })

        elif prediction["failure_probability"] >= 50:

            alerts.append({

                "level": "WARNING",

                "title": "Failure Risk",

                "message": "Server failure probability is increasing."

            })

        # ======================================
        # No Alerts
        # ======================================

        if len(alerts) == 0:

            alerts.append({

                "level": "NORMAL",

                "title": "Healthy",

                "message": "Server is operating normally."

            })

        return alerts

    # ==========================================
    # Run
    # ==========================================

    def run(self):

        return self.get_alerts()


alerts = ServerAlerts()


# ==========================================
# Testing
# ==========================================

if __name__ == "__main__":

    result = alerts.run()

    print("\n========== SERVER ALERTS ==========\n")

    for alert in result:

        print("--------------------------------")

        print("Level :", alert["level"])

        print("Title :", alert["title"])

        print("Message :", alert["message"])

        print("--------------------------------")