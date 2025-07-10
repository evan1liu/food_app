import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

# --- Your Function (copied from your input) ---
def find_nearby_supermarkets(latitude, longitude, radius_meters=500, keyword="supermarket"):
    """
    Finds nearby supermarkets using Google Places API.

    Args:
        latitude (float): Latitude of the user's location.
        longitude (float): Longitude of the user's location.
        radius_meters (int): Search radius in meters (max 50,000 for keyword search).
        keyword (str): The type of place to search for. 'supermarket' or 'grocery_store' are good.

    Returns:
        list: A list of dictionaries, each representing a supermarket.
              Includes 'name', 'place_id', 'vicinity' (address), 'lat', 'lng'.
    """
    if not GOOGLE_PLACES_API_KEY:
        raise ValueError("GOOGLE_PLACES_API_KEY environment variable not set. Please set it or uncomment the os.environ line for testing.")

    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": radius_meters,
        "type": "supermarket",  # or 'grocery_store'
        "keyword": keyword,
        "key": GOOGLE_PLACES_API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        results = response.json()

        supermarkets = []
        for place in results.get("results", []):
            # You might want to filter out places that are not clearly supermarkets
            # or refine based on 'types' array if 'supermarket' type isn't sufficient.
            supermarkets.append({
                "name": place.get("name"),
                "place_id": place.get("place_id"),
                "address": place.get("vicinity"), # 'vicinity' is a good short address
                "lat": place['geometry']['location']['lat'],
                "lng": place['geometry']['location']['lng']
            })

        # Handle pagination if more results are available (up to 60 total)
        # For simplicity, this example only fetches the first page.
        # You'd look for 'next_page_token' in the response to fetch more.

        return supermarkets

    except requests.exceptions.RequestException as e:
        print(f"Error calling Places API: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# --- Test Input and Execution ---

# 1. Coordinates for Downtown Madison, Wisconsin (near the Capitol)
# These are slightly adjusted from the previous context to a central point for good results.
user_lat = 43.0750
user_lng = -89.3840

print(f"Searching for supermarkets near Latitude: {user_lat}, Longitude: {user_lng}")

nearby_stores = find_nearby_supermarkets(user_lat, user_lng, radius_meters=3000) # Search within 3km

if nearby_stores:
    print("\n--- Found Supermarkets ---")
    for i, store in enumerate(nearby_stores):
        print(f"{i+1}. Name: {store.get('name', 'N/A')}")
        print(f"   Address: {store.get('address', 'N/A')}")
        print(f"   Coordinates: ({store.get('lat', 'N/A')}, {store.get('lng', 'N/A')})")
        print(f"   Place ID: {store.get('place_id', 'N/A')}")
        print("-" * 30)
else:
    print("\nNo supermarkets found or an error occurred. Please check your API key and network connection.")