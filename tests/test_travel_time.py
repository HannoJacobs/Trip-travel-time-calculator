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
                departure_date="2024-01-01",
                departure_time="16:40",
                departure_timezone_utc_offset_in_hours=2,  # UTC+2
                arrival_city="Luanda",
                arrival_date="2024-01-01",
                arrival_time="19:10",
                arrival_timezone_utc_offset_in_hours=1,  # UTC+1
            ),
            Flight(
                departure_city="Luanda",
                departure_date="2024-01-01",
                departure_time="23:00",
                departure_timezone_utc_offset_in_hours=1,  # UTC+1
                arrival_city="Sao Paulo",
                arrival_date="2024-01-02",
                arrival_time="03:30",
                arrival_timezone_utc_offset_in_hours=-3,  # UTC-3
            ),
            Flight(
                departure_city="Sao Paulo",
                departure_date="2024-01-02",
                departure_time="08:35",
                departure_timezone_utc_offset_in_hours=-3,  # UTC-3
                arrival_city="Santiago",
                arrival_date="2024-01-02",
                arrival_time="13:00",
                arrival_timezone_utc_offset_in_hours=-3,  # UTC-3
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights)
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
                departure_date="2024-06-01",
                departure_time="08:00",
                departure_timezone_utc_offset_in_hours=-5,  # UTC-5
                arrival_city="London",
                arrival_date="2024-06-01",
                arrival_time="20:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
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
                departure_date="2024-06-15",
                departure_time="23:00",
                departure_timezone_utc_offset_in_hours=-8,  # UTC-8
                arrival_city="Tokyo",
                arrival_date="2024-06-17",
                arrival_time="07:00",
                arrival_timezone_utc_offset_in_hours=9,  # UTC+9
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
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
                departure_date="2024-07-01",
                departure_time="22:00",
                departure_timezone_utc_offset_in_hours=5.75,  # UTC+5:45
                arrival_city="Doha",
                arrival_date="2024-07-02",
                arrival_time="00:30",
                arrival_timezone_utc_offset_in_hours=3,  # UTC+3
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
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
                departure_date="2024-05-10",
                departure_time="09:00",
                departure_timezone_utc_offset_in_hours=1,  # UTC+1
                arrival_city="CityB",
                arrival_date="2024-05-10",
                arrival_time="11:00",
                arrival_timezone_utc_offset_in_hours=2,  # UTC+2
            ),
            Flight(
                departure_city="CityB",
                departure_date="2024-05-10",
                departure_time="13:00",
                departure_timezone_utc_offset_in_hours=2,  # UTC+2
                arrival_city="CityC",
                arrival_date="2024-05-10",
                arrival_time="15:30",
                arrival_timezone_utc_offset_in_hours=3,  # UTC+3
            ),
            Flight(
                departure_city="CityC",
                departure_date="2024-05-10",
                departure_time="17:00",
                departure_timezone_utc_offset_in_hours=3,  # UTC+3
                arrival_city="CityD",
                arrival_date="2024-05-10",
                arrival_time="20:00",
                arrival_timezone_utc_offset_in_hours=4,  # UTC+4
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights)
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
                departure_date="2024-08-20",
                departure_time="06:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityY",
                arrival_date="2024-08-20",
                arrival_time="08:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            ),
            Flight(
                departure_city="CityY",
                departure_date="2024-08-20",
                departure_time="22:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityZ",
                arrival_date="2024-08-21",
                arrival_time="00:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights)
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
                departure_date="2024-09-01",
                departure_time="10:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityN",
                arrival_date="2024-09-01",
                arrival_time="10:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
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

    @pytest.fixture
    def setup_max_time_zone_difference_flight(self):
        """
        Fixture to set up a flight with the maximum time zone difference (UTC-12 to UTC+14).
        """
        flights = [
            Flight(
                departure_city="Baker Island",
                departure_date="2024-01-01",
                departure_time="00:00",
                departure_timezone_utc_offset_in_hours=-12,  # UTC-12
                arrival_city="Kiritimati Island",
                arrival_date="2024-01-02",
                arrival_time="14:00",
                arrival_timezone_utc_offset_in_hours=14,  # UTC+14
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_max_time_zone_difference_flight(
        self, setup_max_time_zone_difference_flight
    ):
        """
        Test a flight with the maximum time zone difference (UTC-12 to UTC+14).
        """
        calculator = setup_max_time_zone_difference_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 00:00 UTC-12 → 12:00 UTC
        # Arrival UTC: 14:00 UTC+14 → 00:00 UTC (next day)
        # Flight Duration: 12 hours (00:00 UTC next day - 12:00 UTC same day)

        expected_total_air_time = timedelta(hours=12, minutes=0)
        expected_total_travel_time = timedelta(hours=12, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for maximum time zone difference flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for maximum time zone difference flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for maximum time zone difference flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for maximum time zone difference flight."

    @pytest.fixture
    def setup_date_line_crossing_flight(self):
        """
        Fixture to set up a flight that crosses the International Date Line.
        """
        flights = [
            Flight(
                departure_city="Fiji",
                departure_date="2024-01-01",
                departure_time="23:00",
                departure_timezone_utc_offset_in_hours=12,  # UTC+12
                arrival_city="Honolulu",
                arrival_date="2024-01-01",
                arrival_time="14:00",
                arrival_timezone_utc_offset_in_hours=-10,  # UTC-10
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_date_line_crossing_flight(self, setup_date_line_crossing_flight):
        """
        Test a flight that crosses the International Date Line.
        """
        calculator = setup_date_line_crossing_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 23:00 UTC+12 → 11:00 UTC
        # Arrival UTC: 14:00 UTC-10 → 00:00 UTC (next day)
        # Flight Duration: 13 hours (00:00 UTC next day - 11:00 UTC same day)

        expected_total_air_time = timedelta(hours=13, minutes=0)
        expected_total_travel_time = timedelta(hours=13, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for date line crossing flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for date line crossing flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for date line crossing flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for date line crossing flight."

    @pytest.fixture
    def setup_long_haul_flight(self):
        """
        Fixture to set up a long-haul flight spanning multiple days.
        """
        flights = [
            Flight(
                departure_city="Los Angeles",
                departure_date="2024-01-01",
                departure_time="12:00",
                departure_timezone_utc_offset_in_hours=-8,  # UTC-8
                arrival_city="Singapore",
                arrival_date="2024-01-02",
                arrival_time="20:00",
                arrival_timezone_utc_offset_in_hours=8,  # UTC+8
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_long_haul_flight(self, setup_long_haul_flight):
        """
        Test a long-haul flight spanning multiple days.
        """
        calculator = setup_long_haul_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 12:00 UTC-8 → 20:00 UTC
        # Arrival UTC: 20:00 UTC+8 → 12:00 UTC (next day)
        # Flight Duration: 16 hours (12:00 UTC next day - 20:00 UTC same day)

        expected_total_air_time = timedelta(hours=16, minutes=0)
        expected_total_travel_time = timedelta(hours=16, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for long-haul flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for long-haul flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for long-haul flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for long-haul flight."

    @pytest.fixture
    def setup_minimal_layover_flight(self):
        """
        Fixture to set up flights with a minimal layover of 1 minute.
        """
        flights = [
            Flight(
                departure_city="CityA",
                departure_date="2024-01-01",
                departure_time="10:00",
                departure_timezone_utc_offset_in_hours=1,  # UTC+1
                arrival_city="CityB",
                arrival_date="2024-01-01",
                arrival_time="12:00",
                arrival_timezone_utc_offset_in_hours=1,  # UTC+1
            ),
            Flight(
                departure_city="CityB",
                departure_date="2024-01-01",
                departure_time="12:01",
                departure_timezone_utc_offset_in_hours=1,  # UTC+1
                arrival_city="CityC",
                arrival_date="2024-01-01",
                arrival_time="14:00",
                arrival_timezone_utc_offset_in_hours=1,  # UTC+1
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_minimal_layover_flight(self, setup_minimal_layover_flight):
        """
        Test flights with a minimal layover of 1 minute.
        """
        calculator = setup_minimal_layover_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Flight 1:
        # Departure UTC: 10:00 UTC+1 → 09:00 UTC
        # Arrival UTC: 12:00 UTC+1 → 11:00 UTC
        # Duration: 2 hours

        # Flight 2:
        # Departure UTC: 12:01 UTC+1 → 11:01 UTC
        # Arrival UTC: 14:00 UTC+1 → 13:00 UTC
        # Duration: 1 hour 59 minutes
        # Layover: 11:01 UTC - 11:00 UTC = 1 minute

        expected_total_air_time = timedelta(
            hours=3, minutes=59
        )  # Updated from 4h0m to 3h59m
        expected_total_travel_time = timedelta(
            hours=4, minutes=0
        )  # Updated from 3h59m to 4h0m
        expected_total_layover_time = timedelta(minutes=1)
        expected_individual_layovers = [timedelta(minutes=1)]

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for minimal layover flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for minimal layover flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for minimal layover flight does not match expected value."
        assert (
            layover_times == expected_individual_layovers
        ), "Individual layover times do not match expected values."

    @pytest.fixture
    def setup_maximal_layover_flight(self):
        """
        Fixture to set up flights with a maximal layover spanning multiple days.
        """
        flights = [
            Flight(
                departure_city="CityX",
                departure_date="2024-01-01",
                departure_time="08:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityY",
                arrival_date="2024-01-01",
                arrival_time="10:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            ),
            Flight(
                departure_city="CityY",
                departure_date="2024-01-03",
                departure_time="08:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityZ",
                arrival_date="2024-01-03",
                arrival_time="10:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_maximal_layover_flight(self, setup_maximal_layover_flight):
        """
        Test flights with a maximal layover spanning multiple days.
        """
        calculator = setup_maximal_layover_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Flight 1:
        # Departure UTC: 08:00 UTC+0 → 08:00 UTC
        # Arrival UTC: 10:00 UTC+0 → 10:00 UTC
        # Duration: 2 hours

        # Flight 2:
        # Departure UTC: 08:00 UTC+0 → 08:00 UTC (next day)
        # Arrival UTC: 10:00 UTC+0 → 10:00 UTC (next day)
        # Duration: 2 hours
        # Layover: 08:00 UTC next day - 10:00 UTC same day = 22 hours

        expected_total_air_time = timedelta(hours=4, minutes=0)
        expected_total_travel_time = timedelta(
            hours=50, minutes=0
        )  # From 08:00 UTC Jan1 to 10:00 UTC Jan3
        expected_total_layover_time = timedelta(hours=46, minutes=0)
        expected_individual_layovers = [timedelta(hours=46, minutes=0)]

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for maximal layover flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for maximal layover flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for maximal layover flight does not match expected value."
        assert (
            layover_times == expected_individual_layovers
        ), "Individual layover time for maximal layover flight does not match expected value."

    @pytest.fixture
    def setup_rapid_succession_flights(self):
        """
        Fixture to set up flights that occur in rapid succession with minimal layovers.
        """
        flights = [
            Flight(
                departure_city="CityA",
                departure_date="2024-01-01",
                departure_time="09:00",
                departure_timezone_utc_offset_in_hours=2,  # UTC+2
                arrival_city="CityB",
                arrival_date="2024-01-01",
                arrival_time="11:00",
                arrival_timezone_utc_offset_in_hours=2,  # UTC+2
            ),
            Flight(
                departure_city="CityB",
                departure_date="2024-01-01",
                departure_time="11:00",
                departure_timezone_utc_offset_in_hours=2,  # UTC+2
                arrival_city="CityC",
                arrival_date="2024-01-01",
                arrival_time="13:00",
                arrival_timezone_utc_offset_in_hours=2,  # UTC+2
            ),
            Flight(
                departure_city="CityC",
                departure_date="2024-01-01",
                departure_time="13:00",
                departure_timezone_utc_offset_in_hours=2,  # UTC+2
                arrival_city="CityD",
                arrival_date="2024-01-01",
                arrival_time="15:00",
                arrival_timezone_utc_offset_in_hours=2,  # UTC+2
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_rapid_succession_flights(self, setup_rapid_succession_flights):
        """
        Test flights that occur in rapid succession with minimal layovers.
        """
        calculator = setup_rapid_succession_flights
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Flight 1:
        # Departure UTC: 09:00 UTC+2 → 07:00 UTC
        # Arrival UTC: 11:00 UTC+2 → 09:00 UTC
        # Duration: 2 hours

        # Flight 2:
        # Departure UTC: 11:00 UTC+2 → 09:00 UTC
        # Arrival UTC: 13:00 UTC+2 → 11:00 UTC
        # Duration: 2 hours
        # Layover: 09:00 UTC - 09:00 UTC = 0 minutes

        # Flight 3:
        # Departure UTC: 13:00 UTC+2 → 11:00 UTC
        # Arrival UTC: 15:00 UTC+2 → 13:00 UTC
        # Duration: 2 hours
        # Layover: 11:00 UTC - 11:00 UTC = 0 minutes

        expected_total_air_time = timedelta(hours=6, minutes=0)
        expected_total_travel_time = timedelta(hours=6, minutes=0)
        expected_total_layover_time = timedelta(minutes=0)
        expected_individual_layovers = [timedelta(minutes=0), timedelta(minutes=0)]

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for rapid succession flights does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for rapid succession flights does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for rapid succession flights does not match expected value."
        assert (
            layover_times == expected_individual_layovers
        ), "Individual layover times for rapid succession flights do not match expected values."

    @pytest.fixture
    def setup_multiple_day_jump_flights(self):
        """
        Fixture to set up flights with layovers spanning multiple days.
        """
        flights = [
            Flight(
                departure_city="CityA",
                departure_date="2024-01-01",
                departure_time="08:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityB",
                arrival_date="2024-01-01",
                arrival_time="10:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            ),
            Flight(
                departure_city="CityB",
                departure_date="2024-01-02",
                departure_time="09:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityC",
                arrival_date="2024-01-02",
                arrival_time="11:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            ),
            Flight(
                departure_city="CityC",
                departure_date="2024-01-03",
                departure_time="10:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="CityD",
                arrival_date="2024-01-03",
                arrival_time="12:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_multiple_day_jump_flights(self, setup_multiple_day_jump_flights):
        """
        Test flights with layovers spanning multiple days.
        """
        calculator = setup_multiple_day_jump_flights
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Flight 1:
        # Departure UTC: 08:00 UTC+0 → 08:00 UTC Jan1
        # Arrival UTC: 10:00 UTC+0 → 10:00 UTC Jan1
        # Duration: 2 hours

        # Flight 2:
        # Departure UTC: 09:00 UTC+0 → 09:00 UTC Jan2
        # Arrival UTC: 11:00 UTC+0 → 11:00 UTC Jan2
        # Duration: 2 hours
        # Layover: 09:00 UTC Jan2 - 10:00 UTC Jan1 = 23 hours

        # Flight 3:
        # Departure UTC: 10:00 UTC+0 → 10:00 UTC Jan3
        # Arrival UTC: 12:00 UTC+0 → 12:00 UTC Jan3
        # Duration: 2 hours
        # Layover: 10:00 UTC Jan3 - 11:00 UTC Jan2 = 23 hours

        expected_total_air_time = timedelta(hours=6, minutes=0)
        expected_total_travel_time = timedelta(
            hours=52, minutes=0
        )  # Updated from 30h0m to 52h0m
        expected_total_layover_time = timedelta(hours=46, minutes=0)
        expected_individual_layovers = [
            timedelta(hours=23, minutes=0),
            timedelta(hours=23, minutes=0),
        ]

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for multiple day jump flights does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for multiple day jump flights does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for multiple day jump flights does not match expected value."
        assert (
            layover_times == expected_individual_layovers
        ), "Individual layover times for multiple day jump flights do not match expected values."

    @pytest.fixture
    def setup_complex_fractional_timezone_flight(self):
        """
        Fixture to set up a flight with a complex fractional UTC offset (e.g., UTC+3:45).
        """
        flights = [
            Flight(
                departure_city="CityA",
                departure_date="2024-01-01",
                departure_time="15:30",
                departure_timezone_utc_offset_in_hours=3.75,  # UTC+3:45
                arrival_city="CityB",
                arrival_date="2024-01-01",
                arrival_time="18:15",
                arrival_timezone_utc_offset_in_hours=5.5,  # UTC+5:30
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_complex_fractional_timezone_flight(
        self, setup_complex_fractional_timezone_flight
    ):
        """
        Test a flight with a complex fractional UTC offset (e.g., UTC+3:45 to UTC+5:30).
        """
        calculator = setup_complex_fractional_timezone_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 15:30 UTC+3:45 → 11:45 UTC
        # Arrival UTC: 18:15 UTC+5:30 → 12:45 UTC
        # Flight Duration: 1 hour (12:45 UTC - 11:45 UTC)

        expected_total_air_time = timedelta(hours=1, minutes=0)
        expected_total_travel_time = timedelta(hours=1, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for complex fractional timezone flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for complex fractional timezone flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for complex fractional timezone flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for complex fractional timezone flight."

    def test_invalid_time_format(self):
        """
        Test that an invalid time format raises a ValueError.
        """
        flights = [
            Flight(
                departure_city="CityA",
                departure_date="2024-01-01",
                departure_time="25:00",  # Invalid time
                departure_timezone_utc_offset_in_hours=0,
                arrival_city="CityB",
                arrival_date="2024-01-01",
                arrival_time="27:00",  # Invalid time
                arrival_timezone_utc_offset_in_hours=0,
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)

        with pytest.raises(ValueError):
            calculator.calculate_travel_times()

    @pytest.fixture
    def setup_dst_transition_flight(self):
        """
        Fixture to set up a flight during DST transition.
        """
        flights = [
            Flight(
                departure_city="New York",
                departure_date="2024-01-01",
                departure_time="01:30",  # During the fall back transition
                departure_timezone_utc_offset_in_hours=-4,  # UTC-4 (EDT)
                arrival_city="London",
                arrival_date="2024-01-01",
                arrival_time="13:30",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_dst_transition_flight(self, setup_dst_transition_flight):
        """
        Test a flight during DST transition.
        """
        calculator = setup_dst_transition_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 01:30 UTC-4 → 05:30 UTC
        # Arrival UTC: 13:30 UTC+0 → 13:30 UTC
        # Flight Duration: 8 hours

        expected_total_air_time = timedelta(hours=8, minutes=0)
        expected_total_travel_time = timedelta(hours=8, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for DST transition flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for DST transition flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for DST transition flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for DST transition flight."

    @pytest.fixture
    def setup_non_standard_minute_offset_flight(self):
        """
        Fixture to set up a flight with a non-standard minute UTC offset (e.g., UTC+5:45).
        """
        flights = [
            Flight(
                departure_city="Kathmandu",
                departure_date="2024-01-01",
                departure_time="15:00",
                departure_timezone_utc_offset_in_hours=5.75,  # UTC+5:45
                arrival_city="Kolkata",
                arrival_date="2024-01-01",
                arrival_time="16:30",
                arrival_timezone_utc_offset_in_hours=5.5,  # UTC+5:30
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_non_standard_minute_offset_flight(
        self, setup_non_standard_minute_offset_flight
    ):
        """
        Test a flight with a non-standard minute UTC offset (e.g., UTC+5:45 to UTC+5:30).
        """
        calculator = setup_non_standard_minute_offset_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 15:00 UTC+5:45 → 09:15 UTC
        # Arrival UTC: 16:30 UTC+5:30 → 11:00 UTC
        # Flight Duration: 1 hour 45 minutes

        expected_total_air_time = timedelta(hours=1, minutes=45)
        expected_total_travel_time = timedelta(hours=1, minutes=45)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for non-standard minute offset flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for non-standard minute offset flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for non-standard minute offset flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for non-standard minute offset flight."

    @pytest.fixture
    def setup_empty_flight_list(self):
        """
        Fixture to set up an empty flight list.
        """
        flights = []
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_empty_flight_list(self, setup_empty_flight_list):
        """
        Test behavior with an empty flight list.
        """
        calculator = setup_empty_flight_list
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        expected_total_air_time = timedelta(0)
        expected_total_travel_time = timedelta(0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for empty flight list should be zero."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for empty flight list should be zero."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for empty flight list should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for empty flight list."

    @pytest.fixture
    def setup_leap_year_flight(self):
        """
        Fixture to set up a flight on February 29th (leap year).
        """
        flights = [
            Flight(
                departure_city="Tokyo",
                departure_date="2024-02-29",
                departure_time="10:00",
                departure_timezone_utc_offset_in_hours=9,  # UTC+9
                arrival_city="Sydney",
                arrival_date="2024-02-29",
                arrival_time="22:00",
                arrival_timezone_utc_offset_in_hours=11,  # UTC+11
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_leap_year_flight(self, setup_leap_year_flight):
        """
        Test a flight on February 29th (leap year).
        """
        calculator = setup_leap_year_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 10:00 UTC+9 → 01:00 UTC
        # Arrival UTC: 22:00 UTC+11 → 11:00 UTC
        # Flight Duration: 10 hours

        expected_total_air_time = timedelta(hours=10, minutes=0)
        expected_total_travel_time = timedelta(hours=10, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for leap year flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for leap year flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for leap year flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for leap year flight."

    @pytest.fixture
    def setup_year_boundary_flight(self):
        """
        Fixture to set up a flight crossing year boundary (Dec 31 to Jan 1).
        """
        flights = [
            Flight(
                departure_city="London",
                departure_date="2023-12-31",
                departure_time="23:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="Sydney",
                arrival_date="2024-01-01",
                arrival_time="10:00",
                arrival_timezone_utc_offset_in_hours=11,  # UTC+11
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_year_boundary_flight(self, setup_year_boundary_flight):
        """
        Test a flight crossing year boundary (Dec 31 to Jan 1).
        """
        calculator = setup_year_boundary_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 23:00 UTC+0 → 23:00 UTC Dec 31
        # Arrival UTC: 10:00 UTC+11 → 23:00 UTC Dec 31 (same time!)
        # Flight Duration: 0 hours

        expected_total_air_time = timedelta(hours=0, minutes=0)
        expected_total_travel_time = timedelta(hours=0, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for year boundary flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for year boundary flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for year boundary flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for year boundary flight."

    @pytest.fixture
    def setup_negative_utc_offset_flights(self):
        """
        Fixture to set up flights with negative UTC offsets.
        """
        flights = [
            Flight(
                departure_city="Los Angeles",
                departure_date="2024-06-15",
                departure_time="08:00",
                departure_timezone_utc_offset_in_hours=-8,  # UTC-8
                arrival_city="Denver",
                arrival_date="2024-06-15",
                arrival_time="11:00",
                arrival_timezone_utc_offset_in_hours=-7,  # UTC-7
            ),
            Flight(
                departure_city="Denver",
                departure_date="2024-06-15",
                departure_time="13:00",
                departure_timezone_utc_offset_in_hours=-7,  # UTC-7
                arrival_city="New York",
                arrival_date="2024-06-15",
                arrival_time="19:00",
                arrival_timezone_utc_offset_in_hours=-5,  # UTC-5
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_negative_utc_offset_flights(self, setup_negative_utc_offset_flights):
        """
        Test flights with negative UTC offsets.
        """
        calculator = setup_negative_utc_offset_flights
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Flight 1:
        # Departure UTC: 08:00 UTC-8 → 16:00 UTC
        # Arrival UTC: 11:00 UTC-7 → 18:00 UTC
        # Duration: 2 hours

        # Flight 2:
        # Departure UTC: 13:00 UTC-7 → 20:00 UTC
        # Arrival UTC: 19:00 UTC-5 → 00:00 UTC (next day)
        # Duration: 4 hours
        # Layover: 20:00 UTC - 18:00 UTC = 2 hours

        expected_total_air_time = timedelta(hours=6, minutes=0)
        expected_total_travel_time = timedelta(hours=8, minutes=0)
        expected_total_layover_time = timedelta(hours=2, minutes=0)
        expected_individual_layovers = [timedelta(hours=2, minutes=0)]

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for negative UTC offset flights does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for negative UTC offset flights does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for negative UTC offset flights does not match expected value."
        assert (
            layover_times == expected_individual_layovers
        ), "Individual layover times for negative UTC offset flights do not match expected values."

    def test_overlapping_flight_times(self):
        """
        Test that overlapping flight times (departure before previous arrival) raise an error.
        """
        flights = [
            Flight(
                departure_city="CityA",
                departure_date="2024-01-01",
                departure_time="10:00",
                departure_timezone_utc_offset_in_hours=0,
                arrival_city="CityB",
                arrival_date="2024-01-01",
                arrival_time="12:00",
                arrival_timezone_utc_offset_in_hours=0,
            ),
            Flight(
                departure_city="CityB",
                departure_date="2024-01-01",
                departure_time="11:00",  # Departs before previous flight arrives
                departure_timezone_utc_offset_in_hours=0,
                arrival_city="CityC",
                arrival_date="2024-01-01",
                arrival_time="13:00",
                arrival_timezone_utc_offset_in_hours=0,
            ),
        ]
        calculator = TravelTimeCalculator(flights=flights)

        with pytest.raises(
            ValueError,
            match="Departure time must be after the previous flight's arrival time",
        ):
            calculator.calculate_travel_times()

    def test_arrival_before_departure(self):
        """
        Test that arrival before departure raises an error.
        """
        flights = [
            Flight(
                departure_city="CityA",
                departure_date="2024-01-01",
                departure_time="15:00",
                departure_timezone_utc_offset_in_hours=0,
                arrival_city="CityB",
                arrival_date="2024-01-01",
                arrival_time="10:00",  # Arrives before departure
                arrival_timezone_utc_offset_in_hours=0,
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)

        with pytest.raises(
            ValueError, match="Arrival time cannot be before departure time"
        ):
            calculator.calculate_travel_times()

    def test_invalid_date_format(self):
        """
        Test that invalid date format raises a ValueError.
        """
        flights = [
            Flight(
                departure_city="CityA",
                departure_date="01/01/2024",  # Invalid format
                departure_time="10:00",
                departure_timezone_utc_offset_in_hours=0,
                arrival_city="CityB",
                arrival_date="2024-01-01",
                arrival_time="12:00",
                arrival_timezone_utc_offset_in_hours=0,
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)

        with pytest.raises(ValueError):
            calculator.calculate_travel_times()

    @pytest.fixture
    def setup_extreme_timezone_flight(self):
        """
        Fixture to set up a flight with extreme but valid timezone differences.
        """
        flights = [
            Flight(
                departure_city="Samoa",
                departure_date="2024-01-01",
                departure_time="12:00",
                departure_timezone_utc_offset_in_hours=13,  # UTC+13
                arrival_city="Baker Island",
                arrival_date="2023-12-31",
                arrival_time="15:00",
                arrival_timezone_utc_offset_in_hours=-12,  # UTC-12
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_extreme_timezone_flight(self, setup_extreme_timezone_flight):
        """
        Test a flight with extreme timezone differences that appears to go backwards in time.
        """
        calculator = setup_extreme_timezone_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 12:00 UTC+13 → 23:00 UTC (Dec 31)
        # Arrival UTC: 15:00 UTC-12 → 03:00 UTC (Jan 1)
        # Flight Duration: 4 hours

        expected_total_air_time = timedelta(hours=4, minutes=0)
        expected_total_travel_time = timedelta(hours=4, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for extreme timezone flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for extreme timezone flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for extreme timezone flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for extreme timezone flight."

    @pytest.fixture
    def setup_month_boundary_flight(self):
        """
        Fixture to set up a flight crossing month boundary (Jan 31 to Feb 1).
        """
        flights = [
            Flight(
                departure_city="Tokyo",
                departure_date="2024-01-31",
                departure_time="22:00",
                departure_timezone_utc_offset_in_hours=9,  # UTC+9
                arrival_city="London",
                arrival_date="2024-02-01",
                arrival_time="05:00",
                arrival_timezone_utc_offset_in_hours=0,  # UTC+0
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_month_boundary_flight(self, setup_month_boundary_flight):
        """
        Test a flight crossing month boundary (Jan 31 to Feb 1).
        """
        calculator = setup_month_boundary_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 22:00 UTC+9 → 13:00 UTC Jan 31
        # Arrival UTC: 05:00 UTC+0 → 05:00 UTC Feb 1
        # Flight Duration: 16 hours

        expected_total_air_time = timedelta(hours=16, minutes=0)
        expected_total_travel_time = timedelta(hours=16, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for month boundary flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for month boundary flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for month boundary flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for month boundary flight."

    @pytest.fixture
    def setup_very_long_flight(self):
        """
        Fixture to set up an extremely long flight (theoretical maximum commercial flight duration).
        """
        flights = [
            Flight(
                departure_city="Sydney",
                departure_date="2024-06-01",
                departure_time="06:00",
                departure_timezone_utc_offset_in_hours=10,  # UTC+10
                arrival_city="London",
                arrival_date="2024-06-02",
                arrival_time="06:00",
                arrival_timezone_utc_offset_in_hours=1,  # UTC+1
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_very_long_flight(self, setup_very_long_flight):
        """
        Test an extremely long flight duration.
        """
        calculator = setup_very_long_flight
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 06:00 UTC+10 → 20:00 UTC May 31 (previous day)
        # Arrival UTC: 06:00 UTC+1 → 05:00 UTC Jun 2
        # Flight Duration: 33 hours (from 20:00 UTC May 31 to 05:00 UTC Jun 2)

        expected_total_air_time = timedelta(hours=33, minutes=0)
        expected_total_travel_time = timedelta(hours=33, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for very long flight does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for very long flight does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for very long flight should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for very long flight."

    @pytest.fixture
    def setup_many_short_flights(self):
        """
        Fixture to set up many short flights with minimal layovers (stress test).
        """
        flights = []
        base_date = "2024-03-01"
        current_hour = 8

        for i in range(10):  # 10 flights
            dep_time = f"{current_hour:02d}:00"
            arr_time = f"{current_hour + 1:02d}:00"

            # Handle day transition when hours exceed 23
            dep_date = base_date
            arr_date = base_date

            if current_hour >= 24:
                # Move to next day
                from datetime import datetime, timedelta as td

                date_obj = datetime.strptime(base_date, "%Y-%m-%d") + td(days=1)
                dep_date = date_obj.strftime("%Y-%m-%d")
                dep_time = f"{current_hour - 24:02d}:00"

            if current_hour + 1 >= 24:
                # Arrival is next day
                from datetime import datetime, timedelta as td

                date_obj = datetime.strptime(base_date, "%Y-%m-%d") + td(days=1)
                arr_date = date_obj.strftime("%Y-%m-%d")
                arr_time = f"{(current_hour + 1) - 24:02d}:00"

            flights.append(
                Flight(
                    departure_city=f"City{i}",
                    departure_date=dep_date,
                    departure_time=dep_time,
                    departure_timezone_utc_offset_in_hours=0,
                    arrival_city=f"City{i+1}",
                    arrival_date=arr_date,
                    arrival_time=arr_time,
                    arrival_timezone_utc_offset_in_hours=0,
                )
            )

            current_hour += 2  # 1 hour flight + 1 hour layover

        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_many_short_flights(self, setup_many_short_flights):
        """
        Test many short flights with minimal layovers (stress test).
        """
        calculator = setup_many_short_flights
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # 10 flights of 1 hour each = 10 hours air time
        # 9 layovers of 1 hour each = 9 hours layover time
        # Total travel time = 19 hours (08:00 to 03:00 next day)

        expected_total_air_time = timedelta(hours=10, minutes=0)
        expected_total_travel_time = timedelta(hours=19, minutes=0)
        expected_total_layover_time = timedelta(hours=9, minutes=0)
        expected_individual_layovers = [timedelta(hours=1, minutes=0)] * 9

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for many short flights does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for many short flights does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for many short flights does not match expected value."
        assert (
            layover_times == expected_individual_layovers
        ), "Individual layover times for many short flights do not match expected values."

    @pytest.fixture
    def setup_utc_zero_flights(self):
        """
        Fixture to set up flights with UTC+0 and UTC-0 (edge case).
        """
        flights = [
            Flight(
                departure_city="London",
                departure_date="2024-04-01",
                departure_time="12:00",
                departure_timezone_utc_offset_in_hours=0,  # UTC+0
                arrival_city="Reykjavik",
                arrival_date="2024-04-01",
                arrival_time="14:00",
                arrival_timezone_utc_offset_in_hours=-0,  # UTC-0 (same as UTC+0)
            )
        ]
        calculator = TravelTimeCalculator(flights=flights)
        return calculator

    def test_utc_zero_flights(self, setup_utc_zero_flights):
        """
        Test flights with UTC+0 and UTC-0 (which should be treated the same).
        """
        calculator = setup_utc_zero_flights
        total_air_time, total_travel_time, total_layover_time, layover_times = (
            calculator.calculate_travel_times()
        )

        # Departure UTC: 12:00 UTC+0 → 12:00 UTC
        # Arrival UTC: 14:00 UTC-0 → 14:00 UTC
        # Flight Duration: 2 hours

        expected_total_air_time = timedelta(hours=2, minutes=0)
        expected_total_travel_time = timedelta(hours=2, minutes=0)
        expected_total_layover_time = timedelta(0)
        expected_individual_layovers = []

        assert (
            total_air_time == expected_total_air_time
        ), "Total air time for UTC zero flights does not match expected value."
        assert (
            total_travel_time == expected_total_travel_time
        ), "Total travel time for UTC zero flights does not match expected value."
        assert (
            total_layover_time == expected_total_layover_time
        ), "Total layover time for UTC zero flights should be zero."
        assert (
            layover_times == expected_individual_layovers
        ), "There should be no layover times for UTC zero flights."
