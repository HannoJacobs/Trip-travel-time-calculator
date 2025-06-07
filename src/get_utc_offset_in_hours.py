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

    except ValueError as original_error:
        # If the original error was from geocoding failure, provide suggestions
        if "Could not find the location" in str(original_error):
            # Try a broader search for suggestions
            try:
                # Split the place name and try partial matches
                words = place_name.split()
                suggestions = []

                for word in words:
                    if len(word) > 2:  # Skip very short words
                        partial_matches = geolocator.geocode(
                            word, exactly_one=False, limit=3
                        )
                        if partial_matches:
                            suggestions.extend(
                                [
                                    f"{loc.address} (lat: {loc.latitude:.2f}, lon: {loc.longitude:.2f})"
                                    for loc in partial_matches[
                                        :2
                                    ]  # Limit to 2 per word
                                ]
                            )

                if suggestions:
                    # Remove duplicates while preserving order
                    unique_suggestions = list(dict.fromkeys(suggestions))
                    raise ValueError(
                        f"Could not find an exact match for '{place_name}'. Did you mean one of these?\n"
                        + "\n".join(unique_suggestions[:5])  # Limit to 5 suggestions
                    )
                else:
                    raise ValueError(
                        f"No matches found for '{place_name}' or similar terms."
                    )
            except Exception:
                raise ValueError(f"No matches found for '{place_name}'.")
        else:
            # Re-raise the original error (e.g., timezone determination failure)
            raise original_error


# Example usage
try:
    place_name = "Luanda Angola"  # Capital of Angola
    timezone_name, utc_offset_hours = get_timezone_with_suggestions(place_name)
    print(
        f"The timezone for {place_name} is {timezone_name}, and the UTC offset is {utc_offset_hours} hours."
    )
except ValueError as e:
    print(e)
