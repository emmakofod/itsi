#!/usr/bin/python3
import sys
import csv

# intanciate 2 dicts (look both ways)

service_to_port = {}
port_to_service = {}

# get file data as csv
with open('./service-names-port-numbers.csv', 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        service_name = row["Service Name"].strip().lower() # Get service names column
        port = row["Port Number"].strip() # Get port numbers column
        
        # Ignore empty values, so check if data
        if service_name and port:
            # For service to port
            if service_name not in service_to_port: 
                service_to_port[service_name] = [] # Don't overwrite data, but add to list
            if port not in service_to_port[service_name]: # Don't get duplicate values
                service_to_port[service_name].append(port)
            
            # For port to service
            if port not in port_to_service:
                port_to_service[port] = []
            if service_name not in port_to_service[port]: 
                port_to_service[port].append(service_name)

# If script is called without argument - error handle
if len(sys.argv) < 2:
    print("You need to give an argument: ./10-service-port.py <service_or_port>")
    sys.exit()

# Get data from the cli
user_input = sys.argv[1].lower()

# Find out which way to look port to service or other way around
if user_input.isdigit():
    if user_input in port_to_service:
        services = port_to_service[user_input]
        print(f"Port {user_input} is for: {', '.join(services)}") # list, format print
    else:
        print("Port not found")
else:
    if user_input in service_to_port:
        ports = service_to_port[user_input]
        print(f"Service {user_input} uses ports: {', '.join(ports)}")
    else:
        print("Service not found")