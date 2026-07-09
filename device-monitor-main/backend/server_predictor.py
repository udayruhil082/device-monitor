from backend.server_analytics import analytics


class ServerPredictor:

    def __init__(self):
        pass

    # ==========================================
    # Prediction
    # ==========================================

    def predict(self):

        data = analytics.get_analytics()

        avg = data["averages"]

        health = data["health_score"]

        trend = data["trend"]

        probability = 0

        # -----------------------
        # CPU
        # -----------------------

        if avg["cpu"] >= 90:
            probability += 30
        elif avg["cpu"] >= 80:
            probability += 20
        elif avg["cpu"] >= 70:
            probability += 10

        # -----------------------
        # RAM
        # -----------------------

        if avg["ram"] >= 90:
            probability += 25
        elif avg["ram"] >= 80:
            probability += 15
        elif avg["ram"] >= 70:
            probability += 8

        # -----------------------
        # Disk
        # -----------------------

        if avg["disk"] >= 95:
            probability += 20
        elif avg["disk"] >= 85:
            probability += 10

        # -----------------------
        # Load
        # -----------------------

        if avg["load"] >= 8:
            probability += 10
        elif avg["load"] >= 5:
            probability += 5

        # -----------------------
        # Trend
        # -----------------------

        if trend == "Degrading":
            probability += 15

        elif trend == "Improving":
            probability -= 10

        # -----------------------
        # Health
        # -----------------------

        probability += int((100 - health) * 0.4)

        probability = max(0, min(100, probability))

        # ======================================
        # Risk Level
        # ======================================

        if probability >= 80:

            risk = "CRITICAL"

        elif probability >= 60:

            risk = "HIGH"

        elif probability >= 40:

            risk = "MEDIUM"

        elif probability >= 20:

            risk = "LOW"

        else:

            risk = "VERY LOW"

        # ======================================
        # Confidence
        # ======================================

        samples = avg["samples"]

        if samples >= 30:

            confidence = 99

        elif samples >= 20:

            confidence = 95

        elif samples >= 10:

            confidence = 90

        elif samples >= 5:

            confidence = 80

        else:

            confidence = 60

        # ======================================
        # Diagnosis
        # ======================================

        diagnosis = []

        if avg["cpu"] > 80:
            diagnosis.append("High CPU utilization detected.")

        if avg["ram"] > 80:
            diagnosis.append("High memory utilization detected.")

        if avg["disk"] > 90:
            diagnosis.append("Disk utilization is approaching capacity.")

        if avg["load"] > 5:
            diagnosis.append("System load is above normal.")

        if trend == "Degrading":
            diagnosis.append("Performance trend is degrading.")

        elif trend == "Improving":
            diagnosis.append("Performance trend is improving.")

        if health >= 90:
            diagnosis.append("Overall server health is excellent.")

        elif health >= 75:
            diagnosis.append("Overall server health is good.")

        elif health >= 60:
            diagnosis.append("Server health requires attention.")

        else:
            diagnosis.append("Server health is critical.")

        if probability >= 80:
            diagnosis.append("Failure probability is very high.")

        if len(diagnosis) == 0:
            diagnosis.append("Server is operating normally.")

        diagnosis = " ".join(diagnosis)

        # ======================================
        # Recommendation
        # ======================================

        if probability >= 80:

            recommendation = (
                "Immediate maintenance is recommended. "
                "Investigate CPU, RAM, Disk and running services."
            )

        elif probability >= 60:

            recommendation = (
                "Schedule preventive maintenance. "
                "Monitor server performance closely."
            )

        elif probability >= 40:

            recommendation = (
                "Continue monitoring. Resource utilization "
                "is increasing."
            )

        elif probability >= 20:

            recommendation = (
                "No immediate action required. Continue monitoring."
            )

        else:

            recommendation = (
                "Server is healthy. No maintenance required."
            )

        return {

            "failure_probability": probability,

            "risk": risk,

            "confidence": confidence,

            "diagnosis": diagnosis,

            "recommendation": recommendation

        }

    # ==========================================
    # Run
    # ==========================================

    def run(self):

        return self.predict()


predictor = ServerPredictor()


if __name__ == "__main__":

    result = predictor.run()

    print("\n========== SERVER PREDICTION ==========\n")

    print("Failure Probability :", result["failure_probability"], "%")

    print("Risk :", result["risk"])

    print("Confidence :", result["confidence"], "%")

    print()

    print("Diagnosis")

    print("--------------------------------")

    print(result["diagnosis"])

    print()

    print("Recommendation")

    print("--------------------------------")

    print(result["recommendation"])