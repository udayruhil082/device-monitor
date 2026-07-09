import paramiko


class ServerService:

    def __init__(self):

        self.host = "192.168.15.51"
        self.username = "support"
        self.password = "Support@817&&"

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

        return stdout.read().decode().strip()
        # ==========================================
    # Hostname
    # ==========================================

    def get_hostname(self):

        return self.run("hostname")
        # ==========================================
    # IP Address
    # ==========================================

    def get_ip(self):

        return self.run("hostname -I")
        # ==========================================
    # Uptime
    # ==========================================
    def get_uptime(self):

     output = self.run("uptime -p")

     output = output.replace("up ", "")

     output = output.replace("days", "Day")

     output = output.replace("day", "Day")

     output = output.replace("hours", "Hr")

     output = output.replace("hour", "Hr")

     output = output.replace("minutes", "Min")

     output = output.replace("minute", "Min")

     return output
        # ==========================================
    # CPU Usage
    # ==========================================

    def get_cpu_usage(self):

        output = self.run("top -bn1")

        for line in output.split("\n"):

            if "%Cpu(s)" in line:

                idle = float(
                    line.split("id,")[0]
                    .split(",")[-1]
                    .strip()
                )

                usage = round(100 - idle, 2)

                return usage

        return 0
          # ==========================================
    # Memory Usage
    # ==========================================

    def get_memory(self):

        output = self.run("free")

        lines = output.split("\n")

        memory = lines[1].split()

        total = int(memory[1])
        used = int(memory[2])
        free = int(memory[3])
        available = int(memory[6])

        usage_percent = round((used / total) * 100, 2)

        return {

            "total": round(total / (1024 ** 2), 2),

            "used": round(used / (1024 ** 2), 2),

            "free": round(free / (1024 ** 2), 2),

            "available": round(available / (1024 ** 2), 2),

            "usage_percent": usage_percent

        }
    
           # ==========================================
    # Disk Usage
    # ==========================================

    def get_disk(self):

        output = self.run("df -h /")

        lines = output.split("\n")

        disk = lines[1].split()

        usage_percent = int(disk[4].replace("%", ""))

        return {

            "filesystem": disk[0],

            "total": disk[1],

            "used": disk[2],

            "free": disk[3],

            "usage": disk[4],

            "usage_percent": usage_percent

        }
        
        # ==========================================
    # Load Average
    # ==========================================

    def get_load_average(self):

        output = self.run("cat /proc/loadavg")

        values = output.split()

        return {
            "1_min": values[0],
            "5_min": values[1],
            "15_min": values[2]
        }
    
          # ==========================================
# Running Processes
# ==========================================

    def get_process_count(self):

        output = self.run("ps -e | wc -l")

        return int(output)
    
    # ==========================================
# Logged In Users
# ==========================================

    def get_logged_users(self):

       output = self.run("who")

       if output.strip() == "":
        return []

       users = []

       for line in output.split("\n"):

        user = line.split()[0]

        users.append(user)

       return users
   
        # ==========================================
    # Operating System
    # ==========================================

    def get_os(self):

        return self.run("cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"'")
      
      
          # ==========================================
    # CPU Information
    # ==========================================

    def get_cpu_info(self):

        output = self.run("lscpu")

        info = {}

        for line in output.split("\n"):

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            info[key.strip()] = value.strip()

        return {

            "model": info.get("Model name", ""),

            "architecture": info.get("Architecture", ""),

            "cores": info.get("Core(s) per socket", ""),

            "threads": info.get("CPU(s)", ""),

            "sockets": info.get("Socket(s)", "")
        }
        
        
      
server = ServerService()