import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from agents.hotel_agent.agent import graph


def test_hotel_agent():

    state = {
        "request": {
            "parameters": {
                "destination": "Tokyo",
                "check_in_date": "2026-06-15"
            }
        }
    }

    result = graph.invoke(state)

    print(result)

def test_hotel_location_filter():

    from agents.hotel_agent.agent import graph

    result = graph.invoke(
        {
            "request": {
                "parameters": {
                    "destination": "Tokyo",
                    "check_in_date": "2026-06-15",
                    "hotel_location_preference": "Shinjuku"
                }
            }
        }
    )

    hotels = result["response"]["results"]

    assert len(hotels) > 0

    for hotel in hotels:

        assert (
            "shinjuku"
            in hotel["distance"].lower()
        )