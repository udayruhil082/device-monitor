"""
gateway_analytics.py

Performs health analysis for the IoT Gateway.
"""

from backend.gateway_service import gateway


class GatewayAnalytics:

    def __init__(self):

        pass
    
        # ==========================================
    # Gateway Analytics
    # ==========================================

    def get_analytics(self):

        data = gateway.get_all_data()

        cpu = data["cpu"]["usage"]

        memory = data["memory"]["usage_percent"]

        lan = data["lan"]["up"]

        airtel = data["airtel"]["up"]

        score = 100

        # ==========================================
        # CPU Health
        # ==========================================

        if cpu >= 90:

            score -= 35

        elif cpu >= 75:

            score -= 20

        elif cpu >= 60:

            score -= 10

        # ==========================================
        # Memory Health
        # ==========================================

        if memory >= 90:

            score -= 30

        elif memory >= 75:

            score -= 20

        elif memory >= 60:

            score -= 10

        # ==========================================
        # LAN Status
        # ==========================================

        if not lan:

            score -= 20

        # ==========================================
        # 5G Status
        # ==========================================

        if not airtel:

            score -= 15

        score = max(score, 0)
        
        # ==========================================
        # Health Status
        # ==========================================

        if score >= 90:

            health_status = "Excellent"

            trend = "Stable"

        elif score >= 75:

            health_status = "Good"

            trend = "Stable"

        elif score >= 60:

            health_status = "Warning"

            trend = "Degrading"

        else:

            health_status = "Critical"

            trend = "Critical"
            
        # ==========================================
        # Return Analytics
        # ==========================================

        return {

            "health_score": score,

            "health_status": health_status,

            "trend": trend,

            "live": data

        }
        
analytics = GatewayAnalytics()
        