# main.py
# Student ID: 012003057

# Import necessary files
import csv
from hashtable import HashTable
from truck import *
from distance import *
from package import *

# Define main function
def main():
    # Initialize hash  table data structures for Trucks 1, 2, and 3
    hash_table = HashTable()
    #Create Trucks with Truck class
    trucks = [Truck(1), Truck(2), Truck(3)]

    # Load address data into variable from CSV file
    address_data = load_address_data('./CSVs/Addresses.csv')
    # Load package data into packages variable from CSV file
    packages = load_package_data('./CSVs/WGUPSPackageFile.csv')
    # Load distance data into variable from CSV file
    distance_data = load_distance_data('./CSVs/WGUPSDistanceTable.csv')
    # Load address names into schedule variable
    schedule = ['4001 South 700 East'] + [pkg['Address'] for pkg in packages]

    #Insert packages data into hash_table
    for package in packages:
        hash_table.insert(package['PackageID'], package['Address'], package['City'], package['State'], package['Zip'], package['DeliveryDeadline'], package['Weight'], package['SpecialNotes'], package['status'])
    # Manually load packages into trucks with truck_assignments variable
    truck_assignments = {
        0: [2,33, 4,40, 7,29, 27,35, 8,30, 10],
        1: [3,18,36,5,37,38, 13,39,14,15,16,19,20,21,34, 23],
        2: [6, 25,26, 28, 31,32, 11, 12, 1, 24, 22, 17, 9]
    }

    # Load packages into trucks 1 and 2 based on truck_assignments dictionary
    for truck_index, package_ids in truck_assignments.items():
        for package_id in package_ids:
            package = hash_table.lookup(package_id)
            trucks[truck_index].add_package((package))

    # Update package statuses to En Route and run delivery algorithm for Truck 1 and Truck 2
    for i in range(2):
        for package in trucks[i].packages:
            package['status'] = 'En Route'
        nearest_neighbor(trucks[i], distance_data, address_data, hash_table)
        # Return trucks 1 and 2 to the hub
        trucks[i].return_to_hub(distance_data, address_data)

    # Determine which truck returns first
    if trucks[0].current_time < trucks[1].current_time:
        trucks[2].current_time = trucks[0].current_time
    else:
        trucks[2].current_time = trucks[1].current_time

    # Update truck 3 package statuses and run nearest neighbor algorithm
    for package in trucks[2].packages:
        package['status'] = 'En Route'
        nearest_neighbor(trucks[2], distance_data, address_data, hash_table)
        # Return truck 3 back to the hub
        trucks[2].return_to_hub(distance_data, address_data)

    # Begin intuitive user interface menu
    while True:
        print("\n********************************************************************************")
        print("1. Print All Packages’ Information: Delivery Time and Total Mileage of all Trucks")
        print("2. Print All Information (including Status) of a given Package at a Given Time")
        print("3. Print All Information (including Statuses) of All the Packages at a Given Time")
        print("4. Exit the Program")
        print("********************************************************************************")

        # Have user input menu choice
        choice = input("Enter your choice: ")

        if choice == '1':
            # Loop through trucks to print individual total mileage
            for truck in trucks:
                print(f"Truck {truck.truck_id} total distance: {truck.total_distance} miles")
                # Loop through the packages in each truck to print package id, address, and delivery time
                for package in truck.route:
                    print(f"\tPackage {package['PackageID']} delivered to {package['Address']} at {package['delivery_time']}")
            # Print total mileage of all trucks
            print(f"Total mileage of all trucks were {total_mileage(trucks)} miles.")
        elif choice == '2':
            # Have user input package id and specified time
            package_id = int(input("Enter Package ID: "))
            chosen_time = input("Enter Time (HH:MM AM/PM): ")
            chosen_time = datetime.strptime(chosen_time, "%I:%M %p")
            # Run individual package info at a specified time
            print_package_info_at_time(package_id, chosen_time, hash_table)
        elif choice == '3':
            # Have user input specified time
            chosen_time = input("Enter Time (HH:MM AM/PM): ")
            chosen_time = datetime.strptime(chosen_time, "%I:%M %p")
            # Loop through package numbers and print individual package info at specified time
            for i in range(1,41):
                print_package_info_at_time(i, chosen_time, hash_table)
        # Break while loop if desired
        elif choice == '4':
            break
        # Print statement if invalid menu option chosen
        else:
            print("Invalid choice. Please try again.")
    # # Display results
    
# Run main function
if __name__ == "__main__":
    main()


    # #Add 13,15, and 19 to the truck with the least amount of packages
    # min_truck = min(trucks, key=lambda truck: len(truck.packages))
    # for package['PackageID'] in [13, 15, 19]:
    #     min_truck.add_package(hash_table.lookup(package['PackageID']))

    # # Separate delayed packages
    # delayed_packages = {6, 25, 28, 32}
    # delayed_until_time = datetime.strptime("09:05 AM", "%I:%M %p")

    # # Assign packages with specific constraints
    # for package in packages:
    #     if package['PackageID'] in delayed_packages:
    #         continue  # Skip delayed packages for now
    #     if 'Can only be on truck 2' in package['SpecialNotes']:
    #         trucks[1].add_package(hash_table.lookup(package['PackageID']))
    #         package['status'] = 'En Route'
    #         print(f"Package {package['PackageID']} status: {package['status']}")
    #     elif package['PackageID'] in {15, 13, 19}:
    #         # These packages must be delivered together
    #         continue  # Skip for now, will add them together later
    #     elif package['PackageID'] == 9:
    #         continue  # Skip package 9 for now
    #     else:
    #         # Find the truck with the least number of packages that has less than 17 packages
    #         min_truck = min(trucks, key=lambda truck: len(truck.packages) if len(truck.packages) < 17 else float('inf'))
    #         min_truck.add_package(hash_table.lookup(package['PackageID']))
    #         package['status'] = 'En Route'
    #         print(f"Package {package['PackageID']} status: {package['status']}")

    # # Add packages 15, 13, and 19 to the same truck
    # min_truck = min(trucks, key=lambda truck: len(truck.packages))
    # for package_id in {15, 13, 19}:
    #     min_truck.add_package(hash_table.lookup(package_id))
    #     package = hash_table.lookup(package_id)
    #     package['status'] = 'En Route'
    #     print(f"Package {package_id} status: {package['status']}")