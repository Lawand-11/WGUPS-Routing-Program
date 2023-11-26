# package.py
from enum import Enum


class SpecialNote(Enum):
    CAN_ONLY_BE_ON_TRUCK_2 = "Can only be on truck 2"
    DELAYED_ON_FLIGHT = "Delayed on flight---will not arrive to depot until 9:05 am"
    WRONG_ADDRESS_LISTED = "Wrong address listed"
    MUST_BE_DELIVERED_WITH = "Must be delivered with"


class PackageStatus(Enum):
    AT_HUB = "At Hub"
    EN_ROUTE = "En Route"
    DELIVERED = "Delivered"


class Package:
    def __init__(
            self,
            package_id,
            address,
            city,
            state,
            zip_code,
            deadline,
            weight,
            special_note=None,
            dependencies=None,
            departure_time=None
    ):
        self.departure_time = departure_time
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_note = special_note
        self.dependencies = dependencies or []
        self.status = PackageStatus.AT_HUB  # Initialize status
        self.time_delivered = None  # Time at which the package is delivered

    def update_status(self, status):
        self.status = status

    def __str__(self):
        return f"Package {self.package_id}"
