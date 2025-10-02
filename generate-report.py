# Import JSON library
import json

# Read json from network_devices.json
data = json.load(open("network_devices.json","r",encoding = "utf-8"))

# Create variables to hold report data
devices_offline = ""
devices_warning = ""
counts = {"switch": 0, "router": 0, "access_point": 0, "load_balancer": 0}
low_uptime = ""
switchport_use= {"total": 0, "used_total": 0}
vlan_used = set()
device_location_and_status = ""

# Read out data on devices
for location in data["locations"]:
     for device in location["devices"]:
        
        # List devices with status "offline"
        if device.get("status") == "offline":
           devices_offline += ( "  " 
                               + device["hostname"].ljust(20) 
                               + device["ip_address"].ljust(20) 
                               + device["type"].ljust(15) 
                               + location["site"] + "\n")
        
        # List devices with status "warning"
        if device.get("status") == "warning":
           # Check if device has low uptime
            if device["uptime_days"] < 10:
               devices_warning += ("  " 
                                   + device["hostname"].ljust(20) 
                                   + device["ip_address"].ljust(20) 
                                   + device["type"].ljust(15) + location["site"].ljust(15) 
                                   + str(device["uptime_days"]).rjust(2) + " dagar upptid\n"
                                   )
        
            # Check for high number of connected devices
            if "connected_clients" in device and device["connected_clients"] > 30:
               devices_warning += ("  " 
                                   + device["hostname"].ljust(20) 
                                   + device["ip_address"].ljust(20) 
                                   + device["type"].ljust(15) 
                                   + location["site"].ljust(15) 
                                   + str(device["connected_clients"]).rjust(2) + " anslutna klienter\n"
                                   )
        
        # Count the total number of devices
        if device.get("type") == "switch":
            counts["switch"] += +1
        if device.get("type") == "router":
            counts["router"] += +1
        if device.get("type") == "access_point":
            counts["access_point"] += +1
        if device.get("type") == "load_balancer":
            counts["load_balancer"] += +1
        
        # List devices witn less than 30 days uptime
        if device.get("uptime_days") <= 30:
            low_uptime += ("  "
                           + device["hostname"].ljust(20) 
                           + location["site"].ljust(15)
                           + str(device["uptime_days"]).rjust(2) + " dagar"  +"\n"
                           )
     
        # get the total number of switchports
        if "ports" in device:
            switchport_use["total"] += device["ports"]["total"]
            switchport_use["used_total"] += device["ports"]["used"]         

        # Get all VLANs used
        if "vlans" in device:
            vlan_used.update(device["vlans"])
        


# Calculate port usage per site
switchport_usage_site_parsed = ""

for location in data["locations"]:

    # store the number of switchports temporary
    switchport_usage_site = {"total": 0, "used": 0}
    
    for device in location["devices"]:
        


        
        if "ports" in device:
            switchport_usage_site["total"] += device["ports"]["total"]
            switchport_usage_site["used"] += device["ports"]["used"]

            #witchport_usage_site_str = str(switchport_usage_site)
        
    switchport_usage_site_percent = (switchport_usage_site["used"] / switchport_usage_site["total"]) * 100
    
    # Round and convert to string
    #switchport_use_site_percent_str = str(round(switchport_usage_site_percent))

    switchport_usage_site_parsed += (location["site"].ljust(20) + " " 
                                        + (str(switchport_usage_site["used"]) + "/" 
                                        + str(switchport_usage_site["total"])).rjust(10) 
                                        + str(round(switchport_usage_site_percent)).rjust(11) + "%\n" )    
    

# Enumerate devices and status per site
device_location_and_status = ""

for location in data["locations"]:
    
    device_location_and_status += (location["site"] +":" + "\n" 
                                   + "  Huvudkontakt: " + location["contact"] + "\n"
                                   )

    # Store temprary statistics
    status_count = {"online": 0, "offline": 0, "warning": 0}
    
    # Count devices and save result in "status_count"
    for device in location["devices"]:
        
        status = device.get("status")
        
        if status == "online":
            status_count["online"] += +1

        if status == "offline":
            status_count["offline"] += +1

        if status == "warning":
            status_count["warning"] += +1

    device_location_and_status += ("  Antal enheter:" +str(len(location["devices"])).rjust(3)
                                   + " (Online: " + str(status_count["online"]) + ","
                                   + " Offline: "  + str(status_count["offline"]) + ","
                                   + " Warning: " + str(status_count["warning"]) +  ")\n\n"
                                   )


# Calculate percentage of use
switchport_use_percentage = (switchport_use["used_total"] / switchport_use["total"]) * 100

#sort values in order
vlan_sorted = sorted(vlan_used)

# Convert integers to string for output in report file
switches = str(counts["switch"])
routers = str(counts["router"])
access_points = str(counts["access_point"])
load_balancers = str(counts["load_balancer"])
switchport_total = str(switchport_use["total"])
switchport_use_total = str(switchport_use["used_total"])
switchport_use_percentage_str = str(round(switchport_use_percentage))
vlan_sorted_str = ", ".join(map(str, vlan_sorted))

# write the report to text file
with open('network_report.txt', 'w', encoding='utf-8') as f:
    f.write("Nätverksrapport - " + data["company"] + "\n")
    f.write("="*50 + "\n")
    f.write("Senast uppdaterad: " + data["last_updated"] + "\n\n")
    f.write("Enheter med problem:\n")
    f.write("-"*30 + "\n")
    f.write("Status: OFFLINE\n")
    f.write(devices_offline + "\n")
    f.write("Status: WARNING\n")
    f.write(devices_warning + "\n")
    f.write("Enheter med mindre än 30 dagars uptime:\n")
    f.write("-"*30 + "\n")
    f.write(low_uptime + "\n")
    f.write("Antal enheter:\n")
    f.write("-"*30 + "\n")
    f.write("Enhetstyp".ljust(20) + "Antal" "\n")
    f.write("  Switch:".ljust(20) + switches.rjust(3) + "\n")
    f.write("  Router:".ljust(20) + routers.rjust(3) + "\n" )
    f.write("  Accesspunkt:".ljust(20) + access_points.rjust(3) + "\n")
    f.write("  Lastbalanserare:".ljust(20) + load_balancers.rjust(3) + "\n\n")
    f.write("portanvändning switchar:\n")
    f.write("-"*30 + "\n")
    f.write("  Totalt: " + switchport_use_total + "/" + switchport_total + " portar används (" + switchport_use_percentage_str + "%)" + "\n\n")
    f.write("VLAN översikt\n")
    f.write("-"*30 + "\n")
    f.write("VLANs: " + vlan_sorted_str + "\n\n")
    f.write("Statistik per site:\n")
    f.write("-"*30 + "\n")
    f.write(device_location_and_status)
    f.write("Switchportanvändning:\n")
    f.write("Site".ljust(18) + "Använt/Totalt" +  "  Användning" "\n")
    f.write(switchport_usage_site_parsed)
