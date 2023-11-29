# main.py
# Lawand Piromari
# Student ID: 011476637
import re
from colorama import Fore, Style, init
from datetime import datetime, timedelta
from algorithm import nearest_neighbor
from hash_table import HashTable
from package import Package, SpecialNote, PackageStatus


def main():
    # initialize colorama for colored text
    init()

    # Initialize the hash table
    package_hash_table = HashTable()

    # Load package data into the hash table
    package_data_string = """
    1	195 W Oakland Ave	Salt Lake City	UT	84115	10:30 AM	21
    2	2530 S 500 E	Salt Lake City	UT	84106	EOD	44	
    3	233 Canyon Rd	Salt Lake City	UT	84103	EOD	2	Can only be on truck 2
    4	380 W 2880 S	Salt Lake City	UT	84115	EOD	4	
    5	410 S State St	Salt Lake City	UT	84111	EOD	5	
    6	3060 Lester St	West Valley City	UT	84119	10:30 AM	88	Delayed on flight---will not arrive to depot until 9:05 am
    7	1330 2100 S	Salt Lake City	UT	84106	EOD	8	
    8	300 State St	Salt Lake City	UT	84103	EOD	9	
    9	300 State St	Salt Lake City	UT	84103	EOD	2	Wrong address listed
    10	600 E 900 South	Salt Lake City	UT	84105	EOD	1	
    11	2600 Taylorsville Blvd	Salt Lake City	UT	84118	EOD	1	
    12	3575 W Valley Central Station bus Loop	West Valley City	UT	84119	EOD	1	
    13	2010 W 500 S	Salt Lake City	UT	84104	10:30 AM	2	Must be delivered with
    14	4300 S 1300 E	Millcreek	UT	84117	10:30 AM	88	Must be delivered with 15, 19
    15	4580 S 2300 E	Holladay	UT	84117	9:00 AM	4	Must be delivered with
    16	4580 S 2300 E	Holladay	UT	84117	10:30 AM	88	Must be delivered with 13, 19
    17	3148 S 1100 W	Salt Lake City	UT	84119	EOD	2	
    18	1488 4800 S	Salt Lake City	UT	84123	EOD	6	Can only be on truck 2
    19	177 W Price Ave	Salt Lake City	UT	84115	EOD	37	Must be delivered with
    20	3595 Main St	Salt Lake City	UT	84115	10:30 AM	37	Must be delivered with 13, 15
    21	3595 Main St	Salt Lake City	UT	84115	EOD	3	
    22	6351 South 900 East	Murray	UT	84121	EOD	2	
    23	5100 South 2700 West	Salt Lake City	UT	84118	EOD	5	
    24	5025 State St	Murray	UT	84107	EOD	7	
    25	5383 South 900 East #104	Salt Lake City	UT	84117	10:30 AM	7	Delayed on flight---will not arrive to depot until 9:05 am
    26	5383 South 900 East #104	Salt Lake City	UT	84117	EOD	25	
    27	1060 Dalton Ave S	Salt Lake City	UT	84104	EOD	5	
    28	2835 Main St	Salt Lake City	UT	84115	EOD	7	Delayed on flight---will not arrive to depot until 9:05 am
    29	1330 2100 S	Salt Lake City	UT	84106	10:30 AM	2	
    30	300 State St	Salt Lake City	UT	84103	10:30 AM	1	
    31	3365 S 900 W	Salt Lake City	UT	84119	10:30 AM	1	
    32	3365 S 900 W	Salt Lake City	UT	84119	EOD	1	Delayed on flight---will not arrive to depot until 9:05 am
    33	2530 S 500 E	Salt Lake City	UT	84106	EOD	1	
    34	4580 S 2300 E	Holladay	UT	84117	10:30 AM	2	
    35	1060 Dalton Ave S	Salt Lake City	UT	84104	EOD	88	
    36	2300 Parkway Blvd	West Valley City	UT	84119	EOD	88	Can only be on truck 2
    37	410 S State St	Salt Lake City	UT	84111	10:30 AM	2	
    38	410 S State St	Salt Lake City	UT	84111	EOD	9	Can only be on truck 2
    39	2010 W 500 S	Salt Lake City	UT	84104	EOD	9	
    40	380 W 2880 S	Salt Lake City	UT	84115	10:30 AM	45	
    """

    # Create a dictionary to map addresses to hub names
    address_to_hub_mapping = {
        "1060 Dalton Ave S": "International Peace Gardens",
        "1330 2100 S": "Sugar House Park",
        "1488 4800 S": "Taylorsville-Bennion Heritage City Gov Off",
        "177 W Price Ave": "Salt Lake City Division of Health Services",
        "195 W Oakland Ave": "South Salt Lake Public Works",
        "2010 W 500 S": "Salt Lake City Streets and Sanitation",
        "2300 Parkway Blvd": "Deker Lake",
        "233 Canyon Rd": "Salt Lake City Ottinger Hall",
        "2530 S 500 E": "Columbus Library",
        "2600 Taylorsville Blvd": "Taylorsville City Hall",
        "2835 Main St": "South Salt Lake Police",
        "300 State St": "Council Hall",
        "3060 Lester St": "Redwood Park",
        "3148 S 1100 W": "Salt Lake County Mental Health",
        "3365 S 900 W": "Salt Lake County/United Police Dept",
        "3575 W Valley Central Station bus Loop": "West Valley Prosecutor",
        "3595 Main St": "Housing Auth. of Salt Lake County",
        "380 W 2880 S": "Utah DMV Administrative Office",
        "410 S State St": "Third District Juvenile Court",
        "4300 S 1300 E": "Cottonwood Regional Softball Complex",
        "4580 S 2300 E": "Holiday City Office",
        "5025 State St": "Murray City Museum",
        "5100 South 2700 West": "Valley Regional Softball Complex",
        "5383 South 900 East #104": "City Center of Rock Springs",
        "600 E 900 South": "Rice Terrace Pavilion Park",
        "6351 South 900 East": "Wheeler Historic Farm"
    }

    package_data_lines = package_data_string.strip().split('\n')[0:]

    for line in package_data_lines:
        # Split the line by tabs to extract package data
        package_info = line.split('\t')

        # Extract package information from the split line
        package_id = int(package_info[0])
        address = address_to_hub_mapping.get(package_info[1], "Unknown Hub")
        city = package_info[2]
        state = package_info[3]
        zip_code = package_info[4]
        deadline = package_info[5]
        weight = int(package_info[6])
        special_notes_str = package_info[7] if len(package_info) > 7 else None

        # Use the SpecialNote enum and capture dependencies if applicable
        special_notes_enum = None
        dependencies = []
        if special_notes_str:
            if 'Must be delivered with' in special_notes_str:
                special_notes_enum = SpecialNote.MUST_BE_DELIVERED_WITH
                # Use regular expression to extract package IDs
                matches = re.findall(r'\d+', special_notes_str)
                dependencies = [int(match) for match in matches]
            else:
                try:
                    special_notes_enum = SpecialNote(special_notes_str)
                except ValueError:
                    print(f"Invalid special note: {special_notes_str}")

        # Create a Package object and add it to the hash table
        package = Package(package_id, address, city, state, zip_code, deadline, weight, special_notes_enum,
                          dependencies)
        package_hash_table.insert(package)

    # Set all packages to a variable
    packages = package_hash_table.get_all_packages()

    # Call the nearest_neighbor function to get the list of Truck objects
    trucks = nearest_neighbor(packages)

    # Print all trucks and their package data
    for truck in trucks:
        print(f"\n{str(truck)}\n")
        truck.deliver_packages()
        print("Packages delivered:")
        for package in truck.route:
            print(f"Package {package.package_id} delivered at {package.time_delivered.strftime('%I:%M %p')}")
        print(f"Total distance driven: {truck.distance_driven} miles")
        print(f"Return Time: {truck.return_time}\n")

    def display_all_packages_status(trucks, user_input_time):
        print(f"{Fore.BLUE}\nPackage statuses at {user_input_time.strftime('%I:%M %p')}:")

        for truck in trucks:
            print(f"{Fore.BLUE}\nTruck {truck.truck_id} - Departure Time: {truck.departure_time}, Miles Driven: {truck.calculate_miles_driven_up_to_time(user_input_time)}")

            for package in truck.route:
                status = get_package_status(package, user_input_time)
                print(f"{Fore.BLUE}Package {package.package_id}: {status}{Style.RESET_ALL}")

    def display_package_status(truck_objects, package_id, user_input_time):
        print(f"{Fore.BLUE}\nPackage {package_id} status at {user_input_time.strftime('%I:%M %p')}:")

        for truck in truck_objects:
            for package in truck.route:
                if package.package_id == package_id:
                    print_current_package_details(package_id)
                    status = get_package_status(package, user_input_time)
                    print(f"Truck {truck.truck_id}: {status}{Style.RESET_ALL}")
                    return

        print(f"{Fore.RED}Package {package_id} not found in any truck.{Style.RESET_ALL}")

    def display_total_mileage(trucks):
        total_mileage = sum(truck.distance_driven for truck in trucks)
        print(f"{Fore.BLUE}\nTotal mileage traveled by all trucks: {total_mileage} miles{Style.RESET_ALL}")

    def get_package_status(package, user_input_time):
        if user_input_time < datetime.strptime(package.departure_time, "%I:%M %p"):
            return f"{Fore.MAGENTA}At the hub, expected delivery at {package.time_delivered.strftime('%I:%M %p')}{Style.RESET_ALL}"
        elif user_input_time < package.time_delivered:
            return f"{Fore.YELLOW}En route, expected delivery at {package.time_delivered.strftime('%I:%M %p')}{Style.RESET_ALL}"
        elif package.status == PackageStatus.DELIVERED:
            return f"{Fore.GREEN}Delivered at {package.time_delivered.strftime('%I:%M %p')}{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}Status not available{Style.RESET_ALL}"

    def get_valid_time_input():
        while True:
            try:
                time_str = input("Enter the time (e.g., 8:35 AM): ")
                user_input_time = datetime.strptime(time_str, "%I:%M %p")
                return user_input_time
            except ValueError:
                print(f"{Fore.RED}Invalid time format. Please enter the time in the format hh:mm AM/PM.{Style.RESET_ALL}")

    def get_valid_package_id_input():
        while True:
            try:
                package_id = int(input("Enter the package ID (e.g., 21): "))
                return package_id
            except ValueError:
                print(f"{Fore.RED}Invalid package ID. Please enter a valid integer.{Style.RESET_ALL}")

    def print_current_package_details(current_package):
        package = package_hash_table.lookup(current_package)
        print(f"Address: {package.address}\n"
              f"Deadline: {package.deadline}\n"
              f"City: {package.city}\n"
              f"Zipcode: {package.zip_code}\n"
              f"Weight: {package.weight} Kilo")

    # loop to start the user interface
    while True:
        print("\nMenu:")
        print("1. Display all packages' statuses at a specific time")
        print("2. Display a specific package's status at a specific time")
        print("3. Display total mileage driven by all trucks")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            user_input_time = get_valid_time_input()
            display_all_packages_status(trucks, user_input_time)

        elif choice == "2":
            package_id = get_valid_package_id_input()
            user_input_time = get_valid_time_input()
            display_package_status(trucks, package_id, user_input_time)

        elif choice == "3":
            display_total_mileage(trucks)

        elif choice == "4":
            print(f"{Fore.RED}Exiting program.{Style.RESET_ALL}")
            break

        else:
            print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 4.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
