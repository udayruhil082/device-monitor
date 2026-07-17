import json
import re
import paramiko


class GatewayService:

    def __init__(self):

        # ==========================================
        # Gateway Credentials
        # ==========================================

        self.host = "192.168.11.1"

        self.username = "root"

        self.password = "ecsd-edge@3682"

        self.client = None

    # ==========================================
    # Connect
    # ==========================================

    def connect(self):

        self.client = paramiko.SSHClient()

        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        self.client.connect(

            hostname=self.host,

            username=self.username,

            password=self.password,

            timeout=10

        )

    # ==========================================
    # Disconnect
    # ==========================================

    def disconnect(self):

        if self.client:

            self.client.close()

    # ==========================================
    # Execute Command
    # ==========================================

    def run(self, command):

        stdin, stdout, stderr = self.client.exec_command(command)

        output = stdout.read().decode().strip()

        return output

    # ==========================================
    # System Board
    # ==========================================

    def get_system_board(self):

        output = self.run(
            "ubus call system board"
        )

        return json.loads(output)

    # ==========================================
    # System Information
    # ==========================================

    def get_system_info(self):

        output = self.run(
            "ubus call system info"
        )

        return json.loads(output)

    # ==========================================
    # LAN Status
    # ==========================================

    def get_lan_status(self):

        output = self.run(
            "ubus call network.interface.lan status"
        )

        return json.loads(output)

    # ==========================================
    # Airtel / 5G Interface
    # ==========================================

    def get_airtel_status(self):

        output = self.run(
            "ubus call network.interface.airtel status"
        )

        return json.loads(output)
    
        # ==========================================
    # Modem Information
    # ==========================================

    def get_modem_info(self):

        output = self.run("mmcli -m 0")

        modem = {}

        for line in output.split("\n"):

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            modem[key.strip()] = value.strip()

        return {

            "manufacturer": modem.get("manufacturer", ""),

            "model": modem.get("model", ""),

            "firmware": modem.get("firmware revision", ""),

            "state": modem.get("state", ""),

            "signal_quality": modem.get("signal quality", ""),

            "operator": modem.get("operator name", ""),

            "imei": modem.get("imei", ""),

            "technology": modem.get("current", "")

        }

    # ==========================================
    # WiFi Information
    # ==========================================

    def get_wifi_info(self):

        output = self.run("iwinfo")

        wifi = {}

        for line in output.split("\n"):

            line = line.strip()

            if "ESSID:" in line:

                wifi["ssid"] = (
                    line.split("ESSID:")[1]
                    .replace('"', "")
                    .strip()
                )

            elif "Channel:" in line:

                wifi["channel"] = (
                    line.split("Channel:")[1]
                    .split("(")[0]
                    .strip()
                )

            elif "Encryption:" in line:

                wifi["encryption"] = (
                    line.split("Encryption:")[1]
                    .strip()
                )

            elif "Mode:" in line:

                wifi["mode"] = (
                    line.split("Mode:")[1]
                    .split("Channel")[0]
                    .strip()
                )

            elif "Hardware:" in line:

                wifi["hardware"] = (
                    line.split("Hardware:")[1]
                    .strip()
                )

        return wifi

    # ==========================================
    # CPU Usage
    # ==========================================

    def get_cpu_usage(self):

        output = self.run("top -bn1")

        match = re.search(
            r"CPU:\s+(\d+)% usr\s+(\d+)% sys.*?(\d+)% idle",
            output
        )

        if match:

            usr = int(match.group(1))

            sys = int(match.group(2))

            idle = int(match.group(3))

            return {

                "usage": usr + sys,

                "idle": idle

            }

        return {

            "usage": 0,

            "idle": 100

        }

    # ==========================================
    # Memory
    # ==========================================

    def get_memory(self):

        output = self.run("free")

        lines = output.split("\n")

        memory = lines[1].split()

        total = int(memory[1])

        used = int(memory[2])

        free = int(memory[3])

        return {

            "total_mb": round(total / 1024, 2),

            "used_mb": round(used / 1024, 2),

            "free_mb": round(free / 1024, 2),

            "usage_percent": round(
                (used / total) * 100,
                2
            )

        }
        
            # ==========================================
    # All Gateway Data
    # ==========================================

    def get_all_data(self):

        self.connect()

        try:

            board = self.get_system_board()

            system = self.get_system_info()

            lan = self.get_lan_status()

            airtel = self.get_airtel_status()

            modem = self.get_modem_info()

            wifi = self.get_wifi_info()

            cpu = self.get_cpu_usage()

            memory = self.get_memory()

            data = {

             "board": board,

             "system": system,

             "cpu": cpu,

             "memory": memory,

             "lan": lan,

             "airtel": airtel,

             "modem": modem,

             "wifi": wifi

}

            print("\n========== AIRTEL ==========")
            print(data["airtel"])

            return data

        finally:

            self.disconnect()


gateway = GatewayService()