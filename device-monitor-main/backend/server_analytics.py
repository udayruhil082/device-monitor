from statistics import mean

from backend.server_service import server
from backend.server_buffer import buffer


class ServerAnalytics:

    def __init__(self):
        pass

    # ==========================================
    # Fetch Live Metrics
    # ==========================================

    def collect_metrics(self):

        server.connect()

        cpu = server.get_cpu_usage()

        memory = server.get_memory()

        disk = server.get_disk()

        load = server.get_load_average()

        processes = server.get_process_count()

        hostname = server.get_hostname()

        ip = server.get_ip()

        uptime = server.get_uptime()

        os_name = server.get_os()

        cpu_info = server.get_cpu_info()

        server.disconnect()

        reading = {

            "cpu": cpu,

            "ram": memory["usage_percent"],

            "disk": disk["usage_percent"],

            "load": float(load["1_min"]),

            "processes": processes

        }

        buffer.add_reading(reading)

        return {

            "hostname": hostname,

            "ip": ip,

            "uptime": uptime,

            "os": os_name,

            "cpu_info": cpu_info,

            "cpu": cpu,

            "memory": memory,

            "disk": disk,

            "load": load,

            "processes": processes

        }
        
            # ==========================================
    # Average Metrics
    # ==========================================

    def get_average_metrics(self):

        readings = buffer.get_readings()

        if len(readings) == 0:

            return None

        avg_cpu = round(
            mean([r["cpu"] for r in readings]), 2
        )

        avg_ram = round(
            mean([r["ram"] for r in readings]), 2
        )

        avg_disk = round(
            mean([r["disk"] for r in readings]), 2
        )

        avg_load = round(
            mean([r["load"] for r in readings]), 2
        )

        avg_processes = round(
            mean([r["processes"] for r in readings]), 2
        )

        return {

            "cpu": avg_cpu,

            "ram": avg_ram,

            "disk": avg_disk,

            "load": avg_load,

            "processes": avg_processes,

            "samples": len(readings)

        }

    # ==========================================
    # Health Score
    # ==========================================

    def calculate_health_score(self):

        avg = self.get_average_metrics()

        if avg is None:

            return 0

        health = 100

        # CPU

        if avg["cpu"] > 95:
            health -= 30

        elif avg["cpu"] > 85:
            health -= 20

        elif avg["cpu"] > 70:
            health -= 10

        # RAM

        if avg["ram"] > 95:
            health -= 30

        elif avg["ram"] > 85:
            health -= 20

        elif avg["ram"] > 70:
            health -= 10

        # Disk

        if avg["disk"] > 95:
            health -= 25

        elif avg["disk"] > 90:
            health -= 15

        elif avg["disk"] > 80:
            health -= 5

        # Load

        if avg["load"] > 10:
            health -= 15

        elif avg["load"] > 5:
            health -= 5

        # Processes

        if avg["processes"] > 1000:
            health -= 10

        if health < 0:
            health = 0

        return health
    
        # ==========================================
    # Trend Detection
    # ==========================================

    def detect_trend(self):

        readings = buffer.get_readings()

        if len(readings) < 5:

            return "Insufficient Data"

        first_half = readings[:len(readings)//2]
        second_half = readings[len(readings)//2:]

        first_cpu = mean([r["cpu"] for r in first_half])
        second_cpu = mean([r["cpu"] for r in second_half])

        difference = second_cpu - first_cpu

        if difference > 5:

            return "Degrading"

        elif difference < -5:

            return "Improving"

        else:

            return "Stable"

    # ==========================================
    # Health Status
    # ==========================================

    def get_health_status(self, health):

        if health >= 90:

            return "Excellent"

        elif health >= 75:

            return "Good"

        elif health >= 60:

            return "Warning"

        else:

            return "Critical"

    # ==========================================
    # Analytics Result
    # ==========================================

    def get_analytics(self):

        live = self.collect_metrics()

        averages = self.get_average_metrics()

        health = self.calculate_health_score()

        trend = self.detect_trend()

        status = self.get_health_status(health)

        return {

            "live": live,

            "averages": averages,

            "health_score": health,

            "health_status": status,

            "trend": trend

        }
        
            # ==========================================
    # Complete Analytics Pipeline
    # ==========================================

    def run(self):

        return self.get_analytics()


# ==========================================
# Singleton Object
# ==========================================

analytics = ServerAnalytics()


# ==========================================
# Testing
# ==========================================

if __name__ == "__main__":

    result = analytics.run()

    print("\n========== SERVER ANALYTICS ==========\n")

    print("Hostname :", result["live"]["hostname"])

    print("IP :", result["live"]["ip"])

    print("CPU :", result["live"]["cpu"])

    print("RAM :", result["live"]["memory"]["usage_percent"])

    print("Disk :", result["live"]["disk"]["usage_percent"])

    print("Load :", result["live"]["load"]["1_min"])

    print("Processes :", result["live"]["processes"])

    print("\n---------- AVERAGES ----------")

    print(result["averages"])

    print("\n---------- HEALTH ----------")

    print("Health Score :", result["health_score"])

    print("Status :", result["health_status"])

    print("Trend :", result["trend"])