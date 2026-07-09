import paramiko

HOST = "192.168.15.51"
USERNAME = "support"
PASSWORD = "Support@817&&"


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(
        hostname=HOST,
        username=USERNAME,
        password=PASSWORD,
        timeout=10
    )

    print("✅ Connected Successfully!")

    stdin, stdout, stderr = client.exec_command("uptime")

    print(stdout.read().decode())

    client.close()

except Exception as e:
    print("❌ Error:", e)