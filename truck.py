from datetime import datetime, timedelta
from distance import *

# Initialize Truck Class with truck ID, package,  route, current location, and total distance information
class Truck:
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []
        self.route = []
        # Initialize current location to be at the hub
        self.current_location = "4001 South 700 East"
        self.total_distance = 0
        # Initialize current time to default the start of the day at 8AM
        self.current_time = datetime.strptime("08:00 AM", "%I:%M %p")

    # Define add package function.
    def add_package(self, package):
        self.packages.append(package)

    # Define delivery package function.
    def deliver_package(self, package, delivery_time):
        #Update package status of package when delivered
        package['status'] = "Delivered"
        # Define delivery time of package.
        package['delivery_time'] = delivery_time
        # Add package to route
        self.route.append(package)
        # Remove  package from truck when delivered
        self.packages.remove(package)

    #Define function to have truck return to hub
    def return_to_hub(self, distance_data, address_data):
        if self.current_location != "Hub":
            # Calculate distance to hub and add it to total distance traveled by truck
            distance_to_hub = distance_between(self.current_location, '4001 South 700 East', address_data, distance_data)
            self.total_distance += distance_to_hub
            
            #Calculate time to drive to hub and update current time of truck and location
            travel_time_to_hub = travel_time(distance_to_hub)
            self.current_time += travel_time_to_hub
            self.current_location = "Hub"
            print(f"Truck {self.truck_id} returned to Hub at {self.current_time.strftime('%I:%M %p')}")