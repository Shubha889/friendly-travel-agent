MOCK_FLIGHTS = {

    ("Chennai", "Tokyo"): [

        {
            "airline": "Air India",
            "flight_number": "AI305",
            "origin": "Chennai",
            "destination": "Tokyo",
            "departure": "07:30",
            "arrival": "19:00",
            "price": 600
        },

        {
            "airline": "ANA",
            "flight_number": "NH777",
            "origin": "Chennai",
            "destination": "Tokyo",
            "departure": "12:30",
            "arrival": "23:00",
            "price": 670
        }
    ],

    ("Chennai", "Paris"): [

        {
            "airline": "Lufthansa",
            "flight_number": "LH761",
            "origin": "Chennai",
            "destination": "Paris",
            "departure": "21:00",
            "arrival": "08:00",
            "price": 890
        },

        {
            "airline": "Air France",
            "flight_number": "AF225",
            "origin": "Chennai",
            "destination": "Paris",
            "departure": "04:00",
            "arrival": "15:00",
            "price": 920
        }
    ],

    ("Chennai", "Singapore"): [

        {
            "airline": "Air India",
            "flight_number": "AI348",
            "origin": "Chennai",
            "destination": "Singapore",
            "departure": "11:00",
            "arrival": "16:30",
            "price": 250
        },

        {
            "airline": "Singapore Airlines",
            "flight_number": "SQ529",
            "origin": "Chennai",
            "destination": "Singapore",
            "departure": "08:15",
            "arrival": "14:00",
            "price": 280
        }
    ],

    ("Bangalore", "Tokyo"): [

        {
            "airline": "Japan Airlines",
            "flight_number": "JL445",
            "origin": "Bangalore",
            "destination": "Tokyo",
            "departure": "09:00",
            "arrival": "20:15",
            "price": 710
        },

        {
            "airline": "ANA",
            "flight_number": "NH812",
            "origin": "Bangalore",
            "destination": "Tokyo",
            "departure": "13:45",
            "arrival": "23:50",
            "price": 740
        }
    ],

    ("Bangalore", "Singapore"): [

        {
            "airline": "Singapore Airlines",
            "flight_number": "SQ503",
            "origin": "Bangalore",
            "destination": "Singapore",
            "departure": "06:00",
            "arrival": "11:20",
            "price": 230
        },

        {
            "airline": "IndiGo",
            "flight_number": "6E1103",
            "origin": "Bangalore",
            "destination": "Singapore",
            "departure": "15:00",
            "arrival": "20:30",
            "price": 210
        }
    ],

    ("Singapore", "Tokyo"): [

        {
            "airline": "Singapore Airlines",
            "flight_number": "SQ638",
            "origin": "Singapore",
            "destination": "Tokyo",
            "departure": "08:00",
            "arrival": "16:15",
            "price": 550
        },

        {
            "airline": "Japan Airlines",
            "flight_number": "JL036",
            "origin": "Singapore",
            "destination": "Tokyo",
            "departure": "14:20",
            "arrival": "22:30",
            "price": 590
        }
    ]
}


def search_flights(
    origin,
    destination
):

    return MOCK_FLIGHTS.get(
        (
            origin.title(),
            destination.title()
        ),
        []
    )