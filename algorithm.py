# algorithm.py

from distance_calculator import calculate_distance_between_hubs
from package import SpecialNote
from truck import Truck

MAX_PACKAGES_PER_TRUCK = 16


def nearest_neighbor(packages):
    remaining_packages = set(packages)

    # Instantiate trucks with departure times
    truck1 = Truck(truck_id=1, departure_time="8:00 AM")
    truck2 = Truck(truck_id=2, departure_time="9:05 AM")
    truck3 = Truck(truck_id=3, departure_time="10:20 AM")

    # Add packages with specific requirements to Truck 2
    for pkg in remaining_packages.copy():
        if pkg.special_note == SpecialNote.CAN_ONLY_BE_ON_TRUCK_2 or pkg.special_note == SpecialNote.DELAYED_ON_FLIGHT:
            if len(truck2.route) < MAX_PACKAGES_PER_TRUCK:
                pkg.departure_time = truck2.departure_time
                truck2.add_package(pkg)
                remaining_packages.remove(pkg)

    # Add packages with the wrong address to truck 3
    for pkg in remaining_packages.copy():
        if pkg.special_note == SpecialNote.WRONG_ADDRESS_LISTED:
            if len(truck3.route) < MAX_PACKAGES_PER_TRUCK:
                pkg.departure_time = truck3.departure_time
                truck3.add_package(pkg)
                remaining_packages.remove(pkg)

    # Add packages that must be delivered together to truck 1 for simplicity
    for pkg in remaining_packages.copy():
        if pkg.special_note == SpecialNote.MUST_BE_DELIVERED_WITH:
            if len(truck1.route) < MAX_PACKAGES_PER_TRUCK:
                pkg.departure_time = truck1.departure_time
                truck1.add_package(pkg)
                remaining_packages.remove(pkg)

    # Add packages with a deadline to truck 1, since it departs earliest
    for pkg in remaining_packages.copy():
        if pkg.deadline != "EOD":
            if len(truck1.route) < MAX_PACKAGES_PER_TRUCK:
                pkg.departure_time = truck1.departure_time
                truck1.add_package(pkg)
                remaining_packages.remove(pkg)

    # Add remaining packages efficiently
    for pkg in remaining_packages.copy():
        min_distance2 = float('inf')
        min_distance3 = float('inf')

        # Check the packages in truck 2
        for p in truck2.route:
            distance = calculate_distance_between_hubs(p.hub_name, pkg.hub_name)[0]
            if distance < min_distance2:
                min_distance2 = distance

        # Check the packages in truck 3
        for p in truck3.route:
            distance = calculate_distance_between_hubs(p.hub_name, pkg.hub_name)[0]
            if distance < min_distance3:
                min_distance3 = distance

        # Compare the distances and add the package to the appropriate truck
        if min_distance2 <= min_distance3 and len(truck2.route) < MAX_PACKAGES_PER_TRUCK:
            pkg.departure_time = truck2.departure_time
            truck2.add_package(pkg)
            remaining_packages.remove(pkg)

        elif len(truck3.route) < MAX_PACKAGES_PER_TRUCK:
            pkg.departure_time = truck3.departure_time
            truck3.add_package(pkg)
            remaining_packages.remove(pkg)

    optimize_route(truck1)
    optimize_route(truck2)
    optimize_route(truck3)

    return [truck1, truck2, truck3]


def optimize_route(truck):
    """
    Optimize the route for a truck using a nearest neighbor approach.

    Args:
        truck (Truck): The truck object with the initial route.

    Returns:
        float: The estimated arrival time back to the hub.
    """
    current_location = "Western Governors University"
    current_route = [current_location]
    sorted_packages = []

    while truck.route:
        nearest_package = min(
            truck.route,
            key=lambda pkg: calculate_distance_between_hubs(current_location, pkg.hub_name)[1]
        )

        current_route.append(nearest_package.hub_name)
        current_location = nearest_package.hub_name
        truck.route.remove(nearest_package)
        sorted_packages.append(nearest_package)

    # Calculate the time to return to the hub
    distance_to_hub, return_time = calculate_distance_between_hubs(current_location, "Western Governors University")
    current_route.append("Western Governors University")

    # add the sorted packages
    truck.add_packages(sorted_packages)

    return return_time
