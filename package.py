# Initialize Package Class
import csv
from hashtable import HashTable
from datetime import datetime, timedelta

class Package:
    def __init__(self, id, address, city, state, zipcode, delivery_deadline, weight, special_notes, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = status
        self.delivery_time = None

# Load package data from a CSV file
def load_package_data(file_path):
    packages = []
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            packages.append({
                'PackageID': int(row['PackageID']),
                'Address': row['Addresses'],
                'City': row['City'],
                'State': row['State'],
                'Zip': row['Zip'],
                'DeliveryDeadline': row['DeliveryDeadline'],
                'Weight': float(row['Weight']),
                'SpecialNotes': row['SpecialNotes'],
                #Default loading status is at the hub
                'status': 'At The Hub',
                'delivery_time': ''
            })
    return packages

# Update package address for package 9 when needed
def update_package_address(hash_table, package_id, new_address, new_city, new_state, new_zip):
    package = hash_table.lookup(package_id)
    if package:
        package['Address'] = new_address
        package['City'] = new_city
        package['State'] = new_state
        package['Zip'] = new_zip
        print(f"Package {package_id} address updated to {new_address}, {new_city}, {new_state}, {new_zip}")
    else:
        print(f"Package {package_id} not found in the hash table.")

# Define print package information function at specified time
def print_package_info_at_time(package_id, chosen_time, hash_table):
    package = hash_table.lookup(package_id)
    if package:
        formatted_time = chosen_time.strftime("%I:%M %p")
        print(f"Package {package_id} at {formatted_time}:")
        # Print wrong address for package 9 before 10:20AM, otherwise print package address as normal
        if package_id == 9 and chosen_time < datetime.strptime("10:20 AM", "%I:%M %p"):
            print(f"Address: 300 State St,Salt Lake City,UT,84103")
        else:
            print(f"Address: {package['Address']} {package['City']}, {package['State']} {package['zipcode']}")

        print(f"Delivery Deadline: {package['deadline']} | Weight: {package['Weight']} | Special Notes: {package['SpecialNotes']}")
        
        # Define delivery time of package
        delivery_time = datetime.strptime(package['delivery_time'], "%I:%M %p") if package['delivery_time'] else None
        
        # Define status of package
        status = ''

        #If chosen time is past delivery time, update status variable to delivered
        if delivery_time and chosen_time >= delivery_time:
            status = 'Delivered'
        #If package is on the late truck, and en route, update status
        elif chosen_time > datetime.strptime("09:18 AM", "%I:%M %p") and package_id in (6,25,26,28,31,32,11,12,1,24,22,17,9):
            status = 'En route'
        #If package left at 8AM and en route, update status
        elif chosen_time > datetime.strptime("08:00 AM", "%I:%M %p") and package_id not in (6,25,26,28,31,32,11,12,1,24,22,17,9):
            status = 'En Route'
        #If  package has not left the hub, update status
        else:
            status = "At Hub"

        print(f"Status: {status}")
        # Prints delivery time if status is delivered, or 'Delivery Time: None' if status is en route or still at the hub
        if status == 'Delivered':
            formatted_delivery_time = delivery_time.strftime("%I:%M %p")
            print(f"Delivery Time: {formatted_delivery_time}")
        else:
            print("Delivery Time: None")
        print()
    else:
        print(f"Package {package_id} not found.")


