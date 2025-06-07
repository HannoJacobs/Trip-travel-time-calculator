"""Calculates the times"""

from datetime import datetime, timedelta
from typing import List, Tuple, Optional


class Flight:
    """
    Represents a single flight with departure and arrival details.
    """

    def __init__(
        self,
        departure_city: str,
        departure_date: str,
        departure_time: str,
        departure_timezone_utc_offset_in_hours: float,
        arrival_city: str,
        arrival_date: str,
        arrival_time: str,
        arrival_timezone_utc_offset_in_hours: float,
    ):
        self.departure_city = departure_city
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.departure_timezone_utc_offset_in_hours = (
            departure_timezone_utc_offset_in_hours
        )
        self.arrival_city = arrival_city
        self.arrival_date = arrival_date
        self.arrival_time = arrival_time
        self.arrival_timezone_utc_offset_in_hours = arrival_timezone_utc_offset_in_hours


class TravelTimeCalculator:
    """
    Calculates total air time, total travel time, and total layover time for a sequence of flights.
    """

    def __init__(self, flights: List[Flight]):
        """
        Initializes the TravelTimeCalculator.

        :param flights: List of Flight objects representing the itinerary.
        """
        self.flights = flights
        self.layover_times: List[timedelta] = []
        self.total_air_time: timedelta = timedelta()
        self.total_travel_time: timedelta = timedelta()
        self.total_layover_time: timedelta = timedelta()

    def _create_datetime(
        self, date_str: str, time_str: str, timezone_offset: float
    ) -> datetime:
        """
        Create a datetime object from date and time strings with timezone offset.

        :param date_str: Date string in 'YYYY-MM-DD' format
        :param time_str: Time string in 'HH:MM' format
        :param timezone_offset: UTC offset in hours
        :return: UTC datetime object
        """
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            time_obj = datetime.strptime(time_str, "%H:%M").time()
        except ValueError as e:
            raise ValueError(f"Invalid date or time format: {e}")

        # Create local datetime
        local_datetime = datetime.combine(date_obj, time_obj)

        # Convert to UTC
        utc_datetime = local_datetime - timedelta(hours=timezone_offset)

        return utc_datetime

    def calculate_travel_times(
        self,
    ) -> Tuple[timedelta, timedelta, timedelta, List[timedelta]]:
        """
        Calculate total air time, total travel time, total layover time, and individual layover times for the sequence of flights.

        :return: A tuple containing:
            - Total air time as a timedelta object.
            - Total travel time as a timedelta object.
            - Total layover time as a timedelta object.
            - List of individual layover times as timedelta objects.
        """
        # Reset cumulative variables
        self.total_air_time = timedelta()
        self.total_travel_time = timedelta()
        self.total_layover_time = timedelta()
        self.layover_times = []

        if not self.flights:
            return (
                self.total_air_time,
                self.total_travel_time,
                self.total_layover_time,
                self.layover_times,
            )

        # Previous flight's arrival datetime in UTC
        prev_arrival_utc: Optional[datetime] = None
        initial_departure_utc: Optional[datetime] = None
        final_arrival_utc: Optional[datetime] = None

        for index, flight in enumerate(self.flights):
            try:
                # Create departure datetime in UTC
                dep_datetime_utc = self._create_datetime(
                    flight.departure_date,
                    flight.departure_time,
                    flight.departure_timezone_utc_offset_in_hours,
                )

                # Create arrival datetime in UTC
                arr_datetime_utc = self._create_datetime(
                    flight.arrival_date,
                    flight.arrival_time,
                    flight.arrival_timezone_utc_offset_in_hours,
                )

                # Validate that arrival is not before departure (allow equal for zero-duration flights)
                if arr_datetime_utc < dep_datetime_utc:
                    raise ValueError(
                        f"Flight {index + 1}: Arrival time cannot be before departure time"
                    )

                # Calculate layover time if not the first flight
                if prev_arrival_utc:
                    if dep_datetime_utc < prev_arrival_utc:
                        raise ValueError(
                            f"Flight {index + 1}: Departure time must be after the previous flight's arrival time"
                        )

                    layover_duration = dep_datetime_utc - prev_arrival_utc
                    self.layover_times.append(layover_duration)
                    self.total_layover_time += layover_duration

                # Calculate flight duration
                flight_duration = arr_datetime_utc - dep_datetime_utc
                self.total_air_time += flight_duration

                # Set initial departure UTC
                if index == 0:
                    initial_departure_utc = dep_datetime_utc

                # Update final arrival UTC
                final_arrival_utc = arr_datetime_utc

                # Update previous arrival UTC for next iteration
                prev_arrival_utc = arr_datetime_utc

            except Exception as e:
                raise ValueError(f"Error processing flight {index + 1}: {str(e)}")

        # Calculate total travel time
        if initial_departure_utc and final_arrival_utc:
            self.total_travel_time = final_arrival_utc - initial_departure_utc
        else:
            self.total_travel_time = timedelta()

        return (
            self.total_air_time,
            self.total_travel_time,
            self.total_layover_time,
            self.layover_times,
        )

    @staticmethod
    def format_timedelta(td: timedelta) -> str:
        """
        Format a timedelta object into a string of the form 'X hours Y minutes'.

        :param td: timedelta object.
        :return: Formatted string.
        """
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(abs(total_seconds), 3600)
        minutes = remainder // 60
        sign = "-" if total_seconds < 0 else ""
        return f"{sign}{hours} hours {minutes} minutes"

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
        total_air_time, _, _, _ = self.calculate_travel_times()
        return self.format_timedelta(total_air_time)

    def get_total_travel_time(self) -> str:
        """
        Returns the total travel time as a formatted string.

        :return: Total travel time in 'X hours Y minutes' format.
        """
        _, total_travel_time, _, _ = self.calculate_travel_times()
        return self.format_timedelta(total_travel_time)

    def get_total_layover_time(self) -> str:
        """
        Returns the total layover time as a formatted string.

        :return: Total layover time in 'X hours Y minutes' format.
        """
        _, _, total_layover_time, _ = self.calculate_travel_times()
        return self.format_timedelta(total_layover_time)

    def get_individual_layover_times(self) -> List[str]:
        """
        Returns individual layover times as a list of formatted strings.

        :return: List of layover times in 'X hours Y minutes' format.
        """
        _, _, _, layover_times = self.calculate_travel_times()
        return [self.format_timedelta(layover) for layover in layover_times]
