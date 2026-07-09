from server_service import server

server.connect()

print("Hostname :", server.get_hostname())
print("IP :", server.get_ip())
print("Uptime :", server.get_uptime())
print("CPU :", server.get_cpu_usage(), "%")
memory = server.get_memory()

print("")

print("RAM")

print("Total :", memory["total"])

print("Used :", memory["used"])

print("Free :", memory["free"])

print("Available :", memory["available"])

disk = server.get_disk()

print("")
print("DISK")
print("Total :", disk["total"])
print("Used :", disk["used"])
print("Free :", disk["free"])
print("Usage :", disk["usage"])
print("Usage Percent :", disk["usage_percent"])

disk = server.get_disk()

print("")
print("DISK")

print("Filesystem :", disk["filesystem"])

print("Total :", disk["total"])

print("Used :", disk["used"])

print("Free :", disk["free"])

print("Usage :", disk["usage"])

load = server.get_load_average()

print("")
print("LOAD AVERAGE")
print("1 Minute  :", load["1_min"])
print("5 Minutes :", load["5_min"])
print("15 Minutes:", load["15_min"])

processes = server.get_process_count()

print("")
print("RUNNING PROCESSES")
print("Processes :", processes)

users = server.get_logged_users()

print("")
print("LOGGED IN USERS")

for user in users:
    print(user)

print("Total Users :", len(users))

os_name = server.get_os()

print("")
print("OPERATING SYSTEM")
print(os_name)

cpu = server.get_cpu_info()

print("")
print("CPU INFORMATION")

print("Model        :", cpu["model"])

print("Architecture :", cpu["architecture"])

print("Sockets      :", cpu["sockets"])

print("Cores        :", cpu["cores"])

print("Threads      :", cpu["threads"])

server.disconnect()
