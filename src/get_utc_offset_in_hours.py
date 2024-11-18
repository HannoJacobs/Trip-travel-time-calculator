from datetime import datetime

import pytz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim


def get_timezone_with_suggestions(place_name):
    """
    Get the timezone and UTC offset in hours for a given place name.
    If the place name is invalid, suggest the nearest possible matches.

    Args:
        place_name (str): The name of the place (e.g., "New York").

    Returns:
        tuple: A tuple containing the timezone name and the UTC offset in hours.
    """
    geolocator = Nominatim(user_agent="timezone_locator")

    try:
        # Try to geocode the location
        location = geolocator.geocode(place_name, exactly_one=False, limit=3)

        if not location:
            raise ValueError(f"Could not find the location: {place_name}")

        # Select the first match as the most likely correct location
        best_match = location[0]
        latitude = best_match.latitude
        longitude = best_match.longitude

        # Get the timezone using TimezoneFinder
        tf = TimezoneFinder()
        timezone_name = tf.timezone_at(lng=longitude, lat=latitude)
        if not timezone_name:
            raise ValueError(f"Could not determine the timezone for {place_name}")

        # Get the UTC offset in hours
        timezone = pytz.timezone(timezone_name)
        now = datetime.now(timezone)
        utc_offset_hours = now.utcoffset().total_seconds() / 3600

        return timezone_name, utc_offset_hours

    except ValueError:
        # Provide suggestions for similar locations
        nearby_matches = geolocator.geocode(place_name, exactly_one=False, limit=5)
        suggestions = (
            [
                f"{loc.address} (lat: {loc.latitude}, lon: {loc.longitude})"
                for loc in nearby_matches
            ]
            if nearby_matches
            else []
        )

        if suggestions:
            raise ValueError(
                f"Could not find an exact match for '{place_name}'. Did you mean one of these?\n"
                + "\n".join(suggestions)
            )
        else:
            raise ValueError(f"No matches found for '{place_name}'.")


# Example usage
try:
    place_name = "Luanda Angola"  # Intentionally misspelled
    timezone_name, utc_offset_hours = get_timezone_with_suggestions(place_name)
    print(
        f"The timezone for {place_name} is {timezone_name}, and the UTC offset is {utc_offset_hours} hours."
    )
except ValueError as e:
    print(e)
