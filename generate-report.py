# Import JSON library
import json

# Read json from network_devices.json
data = json.load(open("network_devices.json","r",encoding = "utf-8"))

# Create variables to hold report data
devices_offline = ""
devices_warning = ""

# Read out status on devices
for location in data["locations"]:
    for device in location["devices"]:
        # List devices with status "offline"
        if device.get("status") == "offline":
           devices_offline += ("  " + device["hostname"] + "\n")
        # List devices with status "warning"
        if device.get("status") == "warning":
           devices_warning += ("  " + device["hostname"] + "\n")
        if device.get("type") == "switch":
            counts 

# write the report to text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write("Nätverksrapport - " + data["company"] + "\n")
    f.write("="*50 + "\n")
    f.write("Senast uppdaterad: " + data["last_updated"] + "\n\n")
    f.write("Enheter med problem:" + "\n")
    f.write("-"*30 + "\n")
    f.write("Status: OFFLINE" + "\n")
    f.write(devices_offline + "\n")
    f.write("Status: WARNING" + "\n")
    f.write(devices_warning + "\n")
    