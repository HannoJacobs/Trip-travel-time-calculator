"""Example main.py"""

from src.calculator import *


print("\nThere trip:\n")
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

calculator = TravelTimeCalculator(flights=flights, departure_date="2024-01-01")
total_air_time, total_travel_time, total_layover_time, layover_times = (
    calculator.calculate_travel_times()
)

print(f"Total Air Time: {calculator.get_total_air_time()}")
print(f"Total Travel Time: {calculator.get_total_travel_time()}")
print(f"Total Layover Time: {calculator.get_total_layover_time()}")

individual_layovers = calculator.get_individual_layover_times()
for idx, layover in enumerate(individual_layovers, start=1):
    print(f"Layover {idx}: {layover}")


print("\nReturn trip:\n")
flights = [
    Flight(
        departure_city="Santiago",
        departure_time="12:25",
        departure_timezone_utc_offset_in_hours=-3,
        arrival_city="Sao Paulo",
        arrival_time="16:30",
        arrival_timezone_utc_offset_in_hours=-3,  # UTC+1
    ),
    Flight(
        departure_city="Sao Paulo",
        departure_time="18:15",
        departure_timezone_utc_offset_in_hours=-3,  # UTC+1
        arrival_city="Luanda",
        arrival_time="06:30",
        arrival_timezone_utc_offset_in_hours=1,  # UTC-3
    ),
    Flight(
        departure_city="Luanda",
        departure_time="10:20",
        departure_timezone_utc_offset_in_hours=1,  # UTC-3
        arrival_city="Johannesburg",
        arrival_time="14:40",
        arrival_timezone_utc_offset_in_hours=2,  # UTC-3
    ),
]

calculator = TravelTimeCalculator(flights=flights, departure_date="2024-01-01")
total_air_time, total_travel_time, total_layover_time, layover_times = (
    calculator.calculate_travel_times()
)

print(f"Total Air Time: {calculator.get_total_air_time()}")
print(f"Total Travel Time: {calculator.get_total_travel_time()}")
print(f"Total Layover Time: {calculator.get_total_layover_time()}")

individual_layovers = calculator.get_individual_layover_times()
for idx, layover in enumerate(individual_layovers, start=1):
    print(f"Layover {idx}: {layover}")
