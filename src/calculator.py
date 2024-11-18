from datetime import datetime, timedelta
from typing import List, Dict, Tuple


def calculate_travel_times(
    flights: List[Dict[str, str]], base_date: str = "2024-01-01"
) -> Tuple[timedelta, timedelta]:
    """
    Calculate total air time and total travel time for a sequence of flights.

    :param flights: List of flights, each flight is a dict with keys:
                    'departure_city', 'departure_time', 'departure_timezone_utc_offset_in_hours',
                    'arrival_city', 'arrival_time', 'arrival_timezone_utc_offset_in_hours'
                    Times are in 'HH:MM' 24-hour format (local times).
                    Timezone offsets are in UTC offset format (e.g., 2 for UTC+2, -3 for UTC-3).
    :param base_date: The starting date for the first flight in 'YYYY-MM-DD' format.
                      Default is '2024-01-01'.
    :return: A tuple containing:
             - Total air time as a timedelta object.
             - Total travel time as a timedelta object.
    """
    # Initialize base date
    current_date = datetime.strptime(base_date, "%Y-%m-%d")

    # Initialize variables
    total_air_time = timedelta()
    initial_departure_utc = None
    final_arrival_utc = None

    # Previous flight's arrival datetime in UTC
    prev_arrival_utc = None

    for index, flight in enumerate(flights):
        dep_city = flight["departure_city"]
        dep_time_str = flight["departure_time"]
        dep_timezone_offset = flight["departure_timezone_utc_offset_in_hours"]
        arr_city = flight["arrival_city"]
        arr_time_str = flight["arrival_time"]
        arr_timezone_offset = flight["arrival_timezone_utc_offset_in_hours"]

        # Parse local departure and arrival times
        dep_time = datetime.strptime(dep_time_str, "%H:%M").time()
        arr_time = datetime.strptime(arr_time_str, "%H:%M").time()

        # Convert local departure time to UTC datetime
        dep_datetime_local = datetime.combine(current_date, dep_time)
        dep_datetime_utc = dep_datetime_local - timedelta(hours=dep_timezone_offset)

        # If not the first flight, ensure departure is after previous arrival
        if prev_arrival_utc:
            if dep_datetime_utc < prev_arrival_utc:
                # Assume departure is on the next day
                dep_datetime_local += timedelta(days=1)
                dep_datetime_utc = dep_datetime_local - timedelta(
                    hours=dep_timezone_offset
                )
                # Repeat until departure UTC is after previous arrival UTC
                while dep_datetime_utc < prev_arrival_utc:
                    dep_datetime_local += timedelta(days=1)
                    dep_datetime_utc = dep_datetime_local - timedelta(
                        hours=dep_timezone_offset
                    )

        # Convert local arrival time to UTC datetime
        arr_datetime_local = datetime.combine(dep_datetime_local.date(), arr_time)
        arr_datetime_utc = arr_datetime_local - timedelta(hours=arr_timezone_offset)

        # If arrival UTC is before departure UTC, assume arrival is next day
        if arr_datetime_utc < dep_datetime_utc:
            arr_datetime_local += timedelta(days=1)
            arr_datetime_utc = arr_datetime_local - timedelta(hours=arr_timezone_offset)

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


# Example Usage
if __name__ == "__main__":
    # Define flights with updated timezone field names
    flights = [
        {
            "departure_city": "Johannesburg",
            "departure_time": "16:40",
            "departure_timezone_utc_offset_in_hours": 2,  # UTC+2
            "arrival_city": "Luanda",
            "arrival_time": "19:10",
            "arrival_timezone_utc_offset_in_hours": 1,  # UTC+1
        },
        {
            "departure_city": "Luanda",
            "departure_time": "23:00",
            "departure_timezone_utc_offset_in_hours": 1,  # UTC+1
            "arrival_city": "Sao Paulo",
            "arrival_time": "03:30",
            "arrival_timezone_utc_offset_in_hours": -3,  # UTC-3
        },
        {
            "departure_city": "Sao Paulo",
            "departure_time": "08:35",
            "departure_timezone_utc_offset_in_hours": -3,  # UTC-3
            "arrival_city": "Santiago",
            "arrival_time": "13:00",
            "arrival_timezone_utc_offset_in_hours": -3,  # UTC-3
        },
    ]

    # Calculate times
    total_air_time, total_travel_time = calculate_travel_times(flights)

    # Display results
    print(f"Total Air Time: {format_timedelta(total_air_time)}")
    print(f"Total Travel Time: {format_timedelta(total_travel_time)}")
