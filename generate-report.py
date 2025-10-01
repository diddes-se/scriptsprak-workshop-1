# Import JSON library
import json

# Read json from network_devices.json
data = json.load(open("network_devices.json","r",encoding = "utf-8"))

# Create variables to hold report data
devices_offline = ""
devices_warning = ""
counts = {"switch": 0, "router": 0, "access_point": 0, "load_balancer": 0}

# Read out data on devices
for location in data["locations"]:
    for device in location["devices"]:
        # List devices with status "offline"
        if device.get("status") == "offline":
           devices_offline += ("  " + device["hostname"] + "\n")
        # List devices with status "warning"
        if device.get("status") == "warning":
           devices_warning += ("  " + device["hostname"] + "\n")
        # Count the number of devices
        if device.get("type") == "switch":
            counts["switch"] += +1
        if device.get("type") == "router":
            counts["router"] += +1
        if device.get("type") == "access_point":
            counts["access_point"] += +1
        if device.get("type") == "load_balancer":
            counts["load_balancer"] += +1

# Convert integers to string
switches = str(counts["switch"])
routers = str(counts["router"])
access_points = str(counts["access_point"])
load_balancers = str(counts["load_balancer"])


# write the report to text file
with open('network_report.txt', 'w', encoding='utf-8') as f:
    f.write("Nätverksrapport - " + data["company"] + "\n")
    f.write("="*50 + "\n")
    f.write("Senast uppdaterad: " + data["last_updated"] + "\n\n")
    f.write("Enheter med problem:" + "\n")
    f.write("-"*30 + "\n")
    f.write("Status: OFFLINE" + "\n")
    f.write(devices_offline + "\n")
    f.write("Status: WARNING" + "\n")
    f.write(devices_warning + "\n")
    f.write("Antal enheter:\n")
    f.write("-"*30 + "\n")
    f.write("  Switch: " + switches + "\n")
    f.write("  Routrar: " + routers + "\n" )
    f.write("  Accesspunkter: " + access_points + "\n")
    f.write("  Lastbalanserare: " + load_balancers + "\n")