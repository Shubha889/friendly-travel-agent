MOCK_HOTELS = {

    "Tokyo": [

        {
            "name": "Shinjuku Grand Hotel",
            "stars": 5,
            "price_per_night": 180,
            "amenities": [
                "WiFi",
                "Pool",
                "Gym",
                "Breakfast"
            ],
            "distance": "300m from Shinjuku Station",
            "landmark": "Shinjuku"
        },

        {
            "name": "Tokyo Skyline Suites",
            "stars": 5,
            "price_per_night": 220,
            "amenities": [
                "WiFi",
                "Pool",
                "Spa"
            ],
            "distance": "500m from Tokyo Tower",
            "landmark": "Tokyo Tower"
        },

        {
            "name": "Tokyo Comfort Inn",
            "stars": 4,
            "price_per_night": 120,
            "amenities": [
                "WiFi",
                "Breakfast"
            ],
            "distance": "1km from Shinjuku",
            "landmark": "Shinjuku"
        },

        {
            "name": "Sakura Residency",
            "stars": 3,
            "price_per_night": 90,
            "amenities": [
                "WiFi"
            ],
            "distance": "2km from Shinjuku",
            "landmark": "Shinjuku"
        }
    ],

    "Paris": [

        {
            "name": "Eiffel Luxury Suites",
            "stars": 5,
            "price_per_night": 280,
            "amenities": [
                "WiFi",
                "Spa",
                "Breakfast"
            ],
            "distance": "400m from Eiffel Tower",
            "landmark": "Eiffel Tower"
        },

        {
            "name": "Paris Central Hotel",
            "stars": 4,
            "price_per_night": 190,
            "amenities": [
                "WiFi",
                "Gym"
            ],
            "distance": "700m from Louvre Museum",
            "landmark": "Louvre"
        },

        {
            "name": "Budget Paris Stay",
            "stars": 3,
            "price_per_night": 110,
            "amenities": [
                "WiFi"
            ],
            "distance": "1.5km from Eiffel Tower",
            "landmark": "Eiffel Tower"
        }
    ],

    "Singapore": [

        {
            "name": "Marina Bay Grand",
            "stars": 5,
            "price_per_night": 280,
            "amenities": [
                "WiFi",
                "Pool",
                "Spa"
            ],
            "distance": "300m from Marina Bay",
            "landmark": "Marina Bay"
        },

        {
            "name": "Orchard Premium Hotel",
            "stars": 4,
            "price_per_night": 190,
            "amenities": [
                "WiFi",
                "Gym"
            ],
            "distance": "500m from Orchard Road",
            "landmark": "Orchard Road"
        },

        {
            "name": "Singapore Budget Stay",
            "stars": 3,
            "price_per_night": 95,
            "amenities": [
                "WiFi"
            ],
            "distance": "1.5km from Marina Bay",
            "landmark": "Marina Bay"
        }
    ]
}


def search_hotels(
    destination,
    location_preference=""
):

    hotels = MOCK_HOTELS.get(
        destination.title(),
        []
    )

    if not location_preference:

        return hotels

    filtered = []

    for hotel in hotels:

        landmark = hotel.get(
            "landmark",
            ""
        ).lower()

        if (
            location_preference.lower()
            in landmark
        ):

            filtered.append(hotel)

    if filtered:

        return filtered

    return hotels