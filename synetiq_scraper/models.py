class CarTooOldException(Exception):
    """Exception class to handle cars too old."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ERROR: {self.message}"


class NotAvailableOrdometerException(Exception):
    """Exception Class to handle not available ordometer."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ERROR: {self.message}"


class Car:
    def __init__(
            self,
            year=None,
            brand=None,
            model=None,
            odometer=None,
            price=None,
            distance=None,
            hours_left=None,
            minutes_left=None,
            link=None,
            engine_starts=None,
            engine_drives=None,
            avg_price=None,
            avg_price_depreciated=None,
            potential_earning=None,
            gearbox=None,
            engine=None
    ):
        self.year = year
        self.brand = brand
        self.model = model
        self.odometer = odometer
        self.price = price
        self.distance = distance
        self.hours_left = hours_left
        self.minutes_left = minutes_left
        self.car_link = link
        self.engine = engine
        self.engine_starts = engine_starts
        self.engine_drives = engine_drives
        self.avg_price = avg_price
        self.avg_price_depreciated = avg_price_depreciated
        self.potential_earning = potential_earning
        self.gearbox = gearbox

    def __str__(self):
        return (f"Car Details:\n"
                f"Year: {self.year}\n"
                f"Brand: {self.brand}\n"
                f"Model: {self.model}\n"
                f"Odometer: {self.odometer} miles\n"
                f"Gearbox: {self.gearbox}\n"
                f"Price: ${self.price}\n"
                f"Distance: {self.distance} miles\n"
                f"Time Left: {self.hours_left} hours and {self.minutes_left} minutes\n"
                f"Link: {self.car_link}\n"
                f"Engine: {self.engine}\n"
                f"Engine Starts: {self.engine_starts}\n"
                f"Engine Drives: {self.engine_drives}\n"
                f"avg price: {self.avg_price}\n"
                f"avg price depreciated: {self.avg_price_depreciated}\n"
                f"potential earning: {self.potential_earning}\n")
