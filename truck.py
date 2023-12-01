# truck.py
from datetime import datetime, timedelta

from distance_calculator import calculate_distance_between_hubs
from package import PackageStatus


class Truck:
    def __init__(self, truck_id, departure_time):
        self.truck_id = truck_id
        self.departure_time = departure_time
        self.return_time = None
        self.route = []
        self.current_location = "Western Governors University"
        self.time_elapsed = 0
        self.distance_driven = 0

    def add_packages(self, packages):
        for p in packages:
            self.route.append(p)

    def add_package(self, package):
        self.route.append(package)

    def calculate_miles_driven_up_to_time(self, current_time):
        departure_datetime = datetime.strptime(self.departure_time, "%I:%M %p")
        if current_time >= departure_datetime:
            time_difference = current_time - departure_datetime
            time_difference_minutes = time_difference.total_seconds() / 60.0

            # Assuming constant speed of 18 miles per hour
            miles_driven = (18 / 60) * time_difference_minutes
            return miles_driven

        return 0

    def deliver_packages(self):
        if not self.route:
            return  # No packages to deliver

        current_location = "Western Governors University"
        for package in self.route:
            package.update_status(PackageStatus.EN_ROUTE)

        for package in self.route:
            distance, estimated_travel_time = calculate_distance_between_hubs(current_location, package.hub_name)
            current_location = package.hub_name  # Update current location

            # Update truck information
            self.distance_driven += distance
            self.time_elapsed += estimated_travel_time

            # Update package information
            package.time_delivered = datetime.strptime(self.calculate_delivery_time(self.time_elapsed), "%I:%M %p")
            package.update_status(PackageStatus.DELIVERED)

        # Update the time when the truck returns to the hub
        distance_to_hub, return_time = calculate_distance_between_hubs(current_location, "Western Governors University")
        self.distance_driven += distance_to_hub
        self.time_elapsed += return_time
        self.return_time = self.calculate_delivery_time(self.time_elapsed)

    def calculate_delivery_time(self, minutes):
        departure_datetime = datetime.strptime(self.departure_time, "%I:%M %p")
        delivery_datetime = departure_datetime + timedelta(minutes=minutes)
        return delivery_datetime.strftime("%I:%M %p")

    def __str__(self):
        return f"Truck {self.truck_id} - Departure Time: {self.departure_time}"
