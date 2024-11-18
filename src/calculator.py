from datetime import datetime, timedelta
from typing import List, Tuple


class Flight:
    """
    Represents a single flight with departure and arrival details.
    """

    def __init__(
        self,
        departure_city: str,
        departure_time: str,
        departure_timezone_utc_offset_in_hours: float,
        arrival_city: str,
        arrival_time: str,
        arrival_timezone_utc_offset_in_hours: float,
    ):
        """
        Initializes a Flight object.

        :param departure_city: Name of the departure city.
        :param departure_time: Departure time in 'HH:MM' (24-hour) format (local time).
        :param departure_timezone_utc_offset_in_hours: UTC offset for departure city (e.g., 2 for UTC+2).
        :param arrival_city: Name of the arrival city.
        :param arrival_time: Arrival time in 'HH:MM' (24-hour) format (local time).
        :param arrival_timezone_utc_offset_in_hours: UTC offset for arrival city (e.g., -3 for UTC-3).
        """
        self.departure_city = departure_city
        self.departure_time = departure_time
        self.departure_timezone_utc_offset_in_hours = (
            departure_timezone_utc_offset_in_hours
        )
        self.arrival_city = arrival_city
        self.arrival_time = arrival_time
        self.arrival_timezone_utc_offset_in_hours = arrival_timezone_utc_offset_in_hours


class TravelTimeCalculator:
    """
    Calculates total air time and total travel time for a sequence of flights.
    """

    def __init__(self, flights: List[Flight], base_date: str = "2024-01-01"):
        """
        Initializes the TravelTimeCalculator.

        :param flights: List of Flight objects representing the itinerary.
        :param base_date: The starting date for the first flight in 'YYYY-MM-DD' format.
                          Default is '2024-01-01'.
        """
        self.flights = flights
        self.base_date = base_date

    def calculate_travel_times(self) -> Tuple[timedelta, timedelta]:
        """
        Calculate total air time and total travel time for the sequence of flights.

        :return: A tuple containing:
                 - Total air time as a timedelta object.
                 - Total travel time as a timedelta object.
        """
        # Initialize base date
        try:
            current_date = datetime.strptime(self.base_date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid base_date format: {e}")

        # Initialize variables
        total_air_time = timedelta()
        initial_departure_utc = None
        final_arrival_utc = None

        # Previous flight's arrival datetime in UTC
        prev_arrival_utc = None

        for index, flight in enumerate(self.flights):
            dep_city = flight.departure_city
            dep_time_str = flight.departure_time
            dep_timezone_offset = flight.departure_timezone_utc_offset_in_hours
            arr_city = flight.arrival_city
            arr_time_str = flight.arrival_time
            arr_timezone_offset = flight.arrival_timezone_utc_offset_in_hours

            # Parse local departure and arrival times
            try:
                dep_time = datetime.strptime(dep_time_str, "%H:%M").time()
                arr_time = datetime.strptime(arr_time_str, "%H:%M").time()
            except ValueError as e:
                raise ValueError(f"Invalid time format in flight {index + 1}: {e}")

            # Convert local departure time to UTC datetime
            dep_datetime_local = datetime.combine(current_date, dep_time)
            dep_datetime_utc = dep_datetime_local - timedelta(hours=dep_timezone_offset)

            # If not the first flight, ensure departure is after previous arrival
            if prev_arrival_utc:
                if dep_datetime_utc < prev_arrival_utc:
                    # Assume departure is on the next day
                    days_added = 1
                    while dep_datetime_utc < prev_arrival_utc:
                        dep_datetime_local += timedelta(days=1)
                        dep_datetime_utc = dep_datetime_local - timedelta(
                            hours=dep_timezone_offset
                        )
                        days_added += 1
                        if days_added > 365:
                            raise Exception(
                                "Infinite loop detected in flight scheduling."
                            )

            # Convert local arrival time to UTC datetime
            arr_datetime_local = datetime.combine(dep_datetime_local.date(), arr_time)
            arr_datetime_utc = arr_datetime_local - timedelta(hours=arr_timezone_offset)

            # If arrival UTC is before departure UTC, assume arrival is next day
            if arr_datetime_utc < dep_datetime_utc:
                arr_datetime_local += timedelta(days=1)
                arr_datetime_utc = arr_datetime_local - timedelta(
                    hours=arr_timezone_offset
                )

            # Calculate flight duration
            flight_duration = arr_datetime_utc - dep_datetime_utc
            total_air_time += flight_duration

            # Update initial departure UTC
            if index == 0:
                initial_departure_utc = dep_datetime_utc

            # Update final arrival UTC
            final_arrival_utc = arr_datetime_utc

            # Update previous arrival UTC for next iteration
            prev_arrival_utc = arr_datetime_utc

        # Calculate total travel time
        if initial_departure_utc and final_arrival_utc:
            total_travel_time = final_arrival_utc - initial_departure_utc
        else:
            total_travel_time = timedelta()

        return total_air_time, total_travel_time

    @staticmethod
    def format_timedelta(td: timedelta) -> str:
        """
        Format a timedelta object into a string of the form 'X hours Y minutes'.

        :param td: timedelta object.
        :return: Formatted string.
        """
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60
        return f"{hours} hours {minutes} minutes"

    def add_flight(self, flight: Flight):
        """
        Adds a Flight object to the itinerary.

        :param flight: Flight object to be added.
        """
        self.flights.append(flight)

    def get_total_air_time(self) -> str:
        """
        Returns the total air time as a formatted string.

        :return: Total air time in 'X hours Y minutes' format.
        """
        total_air_time, _ = self.calculate_travel_times()
        return self.format_timedelta(total_air_time)

    def get_total_travel_time(self) -> str:
        """
        Returns the total travel time as a formatted string.

        :return: Total travel time in 'X hours Y minutes' format.
        """
        _, total_travel_time = self.calculate_travel_times()
        return self.format_timedelta(total_travel_time)


# Example Usage
if __name__ == "__main__":
    # Define flights with updated timezone field names
    flights = [
        Flight(
            departure_city="Johannesburg",
            departure_time="16:40",
            departure_timezone_utc_offset_in_hours=2,  # UTC+2
            arrival_city="Luanda",
            arrival_time="19:10",
            arrival_timezone_utc_offset_in_hours=1,  # UTC+1
        ),
        Flight(
            departure_city="Luanda",
            departure_time="23:00",
            departure_timezone_utc_offset_in_hours=1,  # UTC+1
            arrival_city="Sao Paulo",
            arrival_time="03:30",
            arrival_timezone_utc_offset_in_hours=-3,  # UTC-3
        ),
        Flight(
            departure_city="Sao Paulo",
            departure_time="08:35",
            departure_timezone_utc_offset_in_hours=-3,  # UTC-3
            arrival_city="Santiago",
            arrival_time="13:00",
            arrival_timezone_utc_offset_in_hours=-3,  # UTC-3
        ),
    ]

    # Initialize the calculator
    calculator = TravelTimeCalculator(flights=flights, base_date="2024-01-01")

    # Calculate times
    total_air_time, total_travel_time = calculator.calculate_travel_times()

    # Display results
    print(f"Total Air Time: {calculator.format_timedelta(total_air_time)}")
    print(f"Total Travel Time: {calculator.format_timedelta(total_travel_time)}")
