# Import necessary files
import csv
from datetime import datetime, timedelta
from main import main
from package import *
from hashtable import HashTable

#Define load distance data function
def load_distance_data(file_path):
    distances = []
    #Import distance matrix data into reader variable
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert each element in the row to a float
            distances.append([float(x) for x in row if x])
    return distances

#Define load address data 
def load_address_data(file_path):
    addresses = []
    # Import address data.
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            addresses.append(row[1])
    return addresses

# Define distance_between function to get distance data matrix coordinates
def distance_between(address1, address2, address_data, distance_data):
    i = address_data.index(address1)
    j = address_data.index(address2)
    return distance_data[i][j]

# Define function to calculate travel time based on distance and traveling 18MPH
def travel_time(distance, speed=18):
    return timedelta(minutes = (float(distance)/speed)*60)

# Define Neighbor Algorithm to Deliver Packages
def nearest_neighbor(truck, distance_data, address_data, hash_table):
    while truck.packages:
        current_location = truck.current_location

        # Initialize the minimum distance and the nearest package
        min_distance = float('inf')
        nearest_package = None

        #Loop through all packages in the truck
        for package in truck.packages:
            # If time passes 10:20 AM, update package 9 address
            if truck.current_time > datetime.strptime("10:20 AM", "%I:%M %p") and hash_table.lookup(9)['Address'] != "410 S State St":
                update_package_address(hash_table, 9, "410 S State St", "Salt Lake City", "UT", "84111")

            # Determine shortest distance between current location and all unvisited packaged addresses
            distance = distance_between(current_location, package['Address'], address_data, distance_data)
            if distance < min_distance:
                # Update variables if new shortest distance found
                min_distance = distance
                nearest_package = package

        # Determine distance to next delivery and what delivery time will be for the next package
        distance_next = distance_between(current_location, nearest_package['Address'], address_data, distance_data)
        delivery_time = truck.current_time + travel_time(distance_next)
        
        # Call deliver package function to update package info
        truck.deliver_package(nearest_package, delivery_time.strftime("%I:%M %p"))
        # Update current truck location
        truck.current_location = nearest_package['Address']
        # Update total distance of the truck
        truck.total_distance += distance_between(current_location, nearest_package['Address'], address_data, distance_data)
        # Update current time to delivery time
        truck.current_time = delivery_time

# Define total mileage function to summation all trucks mileage
def total_mileage(trucks):
    return sum(truck.total_distance for truck in trucks)

