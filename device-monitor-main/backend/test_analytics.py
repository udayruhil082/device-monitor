from server_analytics import analytics

result = analytics.get_health()

print("")

print("SERVER HEALTH")

print("------------------------")

for key, value in result.items():

    print(f"{key} : {value}")