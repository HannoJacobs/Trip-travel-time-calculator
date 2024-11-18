# tests/test_calculator.py

import sys
import os

# Adjust the path to import from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import pytest
from datetime import timedelta
from src.calculator import Flight, TravelTimeCalculator


class TestTravelTimeCalculator:
    @pytest.fixture
    def setup_specific_trip(self):
        """
        Fixture to set up the specific trip from Johannesburg to Santiago via Luanda and Sao Paulo.
        """
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
        calculator = TravelTimeCalculator(flights=flights, base_date="2024-01-01")
        return calculator

    def test_specific_trip_calculations(self, setup_specific_trip):
        """
        Test the specific trip from Johannesburg to Santiago.
        """
        calculator = setup_specific_trip
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Expected results based on corrected calculations
        expected_total_air_time = timedelta(hours=16, minutes=25)
        expected_total_travel_time = timedelta(hours=25, minutes=20)
        expected_total_layover_time = timedelta(hours=8, minutes=55)
        expected_individual_layovers = [
            timedelta(hours=3, minutes=50),
            timedelta(hours=5, minutes=5),
        ]

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time does not match expected value."
        assert (
            layover_times == expected_individual_layovers
        ), "Individual layover times do not match expected values."

    @pytest.fixture
    def setup_single_flight(self):
        """
        Fixture to set up a single flight scenario with no layovers.
        """
        flights = [
            Flight(
                departure_city="New York",
                departure_time="08:00",
                departure_timezone_utc_offset_in_hours=-5,  # UTC-5
                arrival_city="London",
                arrival_time="20:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            )
        ]
        calculator = TravelTimeCalculator(flights=flights, base_date="2024-06-01")
        return calculator

    def test_single_flight_no_layover(self, setup_single_flight):
        """
        Test a scenario with a single flight (no layovers).
        """
        calculator = setup_single_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        expected_total_air_time = timedelta(hours=7, minutes=0)
        expected_total_travel_time = timedelta(hours=7, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for single flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for single flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for single flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for single flight."

    @pytest.fixture
    def setup_cross_midnight_flight(self):
        """
        Fixture to set up flights that cross over midnight.
        """
        flights = [
            Flight(
                departure_city="Los Angeles",
                departure_time="23:00",
                departure_timezone_utc_offset_in_hours=-8,  # UTC-8
                arrival_city="Tokyo",
                arrival_time="07:00",
                arrival_timezone_utc_offset_in_hours=9,  # UTC+9
            )
        ]
        calculator = TravelTimeCalculator(flights=flights, base_date="2024-06-15")
        return calculator

    def test_flights_crossing_midnight(self, setup_cross_midnight_flight):
        """
        Test flights that cross over midnight.
        """
        calculator = setup_cross_midnight_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Expected flight duration: 15 hours
        expected_total_air_time = timedelta(hours=15, minutes=0)
        expected_total_travel_time = timedelta(hours=15, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for overnight flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for overnight flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for overnight flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for single overnight flight."

    @pytest.fixture
    def setup_fractional_timezone_flight(self):
        """
        Fixture to set up a flight with fractional UTC offsets.
        """
        flights = [
            Flight(
                departure_city="Kathmandu",
                departure_time="22:00",
                departure_timezone_utc_offset_in_hours=5.75,  # UTC+5:45
                arrival_city="Doha",
                arrival_time="00:30",
                arrival_timezone_utc_offset_in_hours=3,  # UTC+3
            )
        ]
        calculator = TravelTimeCalculator(flights=flights, base_date="2024-07-01")
        return calculator

    def test_fractional_utc_offsets(self, setup_fractional_timezone_flight):
        """
        Test flights with fractional UTC offsets.
        """
        calculator = setup_fractional_timezone_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Expected flight duration: 5 hours 15 minutes
        expected_total_air_time = timedelta(hours=5, minutes=15)
        expected_total_travel_time = timedelta(hours=5, minutes=15)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for flight with fractional UTC offset does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for flight with fractional UTC offset does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for flight with fractional UTC offset should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for flight with fractional UTC offset."

    @pytest.fixture
    def setup_multiple_layovers(self):
        """
        Fixture to set up a sequence of flights with multiple layovers.
        """
        flights = [
            Flight(
                departure_city="CityA",
                departure_time="09:00",
                departure_timezone_utc_offset_in_hours=1,  # UTC+1
                arrival_city="CityB",
                arrival_time="11:00",
                arrival_timezone_utc_offset_in_hours=2,  # UTC+2
            ),
            Flight(
                departure_city="CityB",
                departure_time="13:00",
                departure_timezone_utc_offset_in_hours=2,  # UTC+2
                arrival_city="CityC",
                arrival_time="15:30",
                arrival_timezone_utc_offset_in_hours=3,  # UTC+3
            ),
            Flight(
                departure_city="CityC",
                departure_time="17:00",
                departure_timezone_utc_offset_in_hours=3,  # UTC+3
                arrival_city="CityD",
                arrival_time="20:00",
                arrival_timezone_utc_offset_in_hours=4,  # UTC+4
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights, base_date="2024-05-10")
        return calculator

    def test_multiple_layovers(self, setup_multiple_layovers):
        """
        Test a sequence of flights with multiple layovers.
        """
        calculator = setup_multiple_layovers
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Calculations:
        # Flight 1:
        # Departure UTC: 09:00 -1 = 08:00 UTC
        # Arrival UTC: 11:00 -2 = 09:00 UTC
        # Duration: 1 hour

        # Flight 2:
        # Departure UTC: 13:00 -2 = 11:00 UTC
        # Arrival UTC: 15:30 -3 = 12:30 UTC
        # Duration: 1 hour 30 minutes
        # Layover: 11:00 UTC - 09:00 UTC = 2 hours

        # Flight 3:
        # Departure UTC: 17:00 -3 = 14:00 UTC
        # Arrival UTC: 20:00 -4 = 16:00 UTC
        # Duration: 2 hours
        # Layover: 14:00 UTC - 12:30 UTC = 1 hour 30 minutes

        expected_total_air_time = (
            timedelta(hours=1, minutes=0)
            + timedelta(hours=1, minutes=30)
            + timedelta(hours=2, minutes=0)
        )  # 4h30m
        expected_total_travel_time = timedelta(
            hours=8, minutes=0
        )  # From 08:00 UTC to 16:00 UTC
        expected_total_layover_time = timedelta(hours=2, minutes=0) + timedelta(
            hours=1, minutes=30
        )  # 3h30m
        expected_individual_layovers = [
            timedelta(hours=2, minutes=0),
            timedelta(hours=1, minutes=30),
        ]

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for multiple layovers does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for multiple layovers does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for multiple layovers does not match expected value."
        assert (
            layover_times == expected_individual_layovers
        ), "Individual layover times for multiple layovers do not match expected values."

    @pytest.fixture
    def setup_large_layover(self):
        """
        Fixture to set up a flight sequence with a large layover.
        """
        flights = [
            Flight(
                departure_city="CityX",
                departure_time="06:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityY",
                arrival_time="08:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            ),
            Flight(
                departure_city="CityY",
                departure_time="22:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityZ",
                arrival_time="00:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights, base_date="2024-08-20")
        return calculator

    def test_large_layover(self, setup_large_layover):
        """
        Test a flight sequence with a large layover.
        """
        calculator = setup_large_layover
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Calculations:
        # Flight 1:
        # Departure UTC: 06:00 -0 =06:00 UTC
        # Arrival UTC: 08:00 -0 =08:00 UTC
        # Duration: 2 hours

        # Flight 2:
        # Departure UTC: 22:00 -0 =22:00 UTC
        # Arrival UTC: 00:00 -0 =00:00 UTC (next day)
        # Duration: 2 hours
        # Layover: 22:00 UTC - 08:00 UTC =14 hours

        expected_total_air_time = timedelta(hours=4, minutes=0)  # 2h + 2h
        expected_total_travel_time = timedelta(
            hours=18, minutes=0
        )  # From 06:00 UTC to 00:00 UTC next day
        expected_total_layover_time = timedelta(hours=14, minutes=0)
        expected_individual_layovers = [timedelta(hours=14, minutes=0)]

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for large layover does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for large layover does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for large layover does not match expected value."
        assert (
            layover_times == expected_individual_layovers
        ), "Individual layover times for large layover do not match expected values."

    @pytest.fixture
    def setup_zero_duration_flight(self):
        """
        Fixture to set up a flight where departure and arrival times are the same (zero duration).
        """
        flights = [
            Flight(
                departure_city="CityM",
                departure_time="10:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityN",
                arrival_time="10:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            )
        ]
        calculator = TravelTimeCalculator(flights=flights, base_date="2024-09-01")
        return calculator

    def test_zero_duration_flight(self, setup_zero_duration_flight):
        """
        Test a flight where departure and arrival times are the same (zero duration).
        """
        calculator = setup_zero_duration_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        expected_total_air_time = timedelta(hours=0, minutes=0)
        expected_total_travel_time = timedelta(hours=0, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for zero duration flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for zero duration flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for zero duration flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for zero duration flight."


if __name__ == "__main__":
    pytest.main()
