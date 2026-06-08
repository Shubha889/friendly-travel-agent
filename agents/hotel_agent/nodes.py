from typing import TypedDict
from .mock_data import MOCK_HOTELS
from datetime import datetime


class HotelState(TypedDict):
    request: dict
    hotels: list
    response: dict


def validate_input(state: HotelState):

    request = state["request"]

    params = request["parameters"]

    required = [
        "destination",
        "check_in_date"
    ]

    missing = []

    for field in required:

        if not params.get(field):
            missing.append(field)

    if missing:

        state["response"] = {
            "status": "needs_clarification",
            "clarification_needed":
                f"Missing fields: {', '.join(missing)}"
        }

    return state

def search_hotels(state: HotelState):

    if state.get("response"):
        return state

    params = state["request"]["parameters"]

    destination = (
        params.get(
            "destination",
            ""
        )
        .strip()
        .title()
    )

    location_preference = (
        params.get(
            "hotel_location_preference",
            ""
        )
        .strip()
        .lower()
    )

    matching_hotels = MOCK_HOTELS.get(
        destination,
        []
    )

    if location_preference:

        filtered_hotels = []

        for hotel in matching_hotels:

            searchable_text = (
                hotel.get(
                    "landmark",
                    ""
                ).lower()
                + " "
                +
                hotel.get(
                    "distance",
                    ""
                ).lower()
            )

            if (
                location_preference
                in searchable_text
            ):
                filtered_hotels.append(
                    hotel
                )

        if filtered_hotels:
            matching_hotels = filtered_hotels

    matching_hotels = sorted(
        matching_hotels,
        key=lambda x: x["price_per_night"]
    )

    state["hotels"] = matching_hotels

    return state
def format_response(state: HotelState):

    if state.get("response"):
        return state

    hotels = state.get(
        "hotels",
        []
    )

    if not hotels:

        state["response"] = {
            "task_id": state["request"].get(
                "task_id",
                "hotel-task"
            ),
            "status": "failed",
            "results": [],
            "clarification_needed": None,
            "error":
                "No hotels available for this destination",
            "metadata": {
                "agent_id": "hotel-agent",
                "timestamp": datetime.utcnow().isoformat()
            }
        }

        return state

    state["response"] = {
        "task_id": state["request"].get(
            "task_id",
            "hotel-task"
        ),
        "status": "success",
        "results": hotels,
        "clarification_needed": None,
        "error": None,
        "metadata": {
            "agent_id": "hotel-agent",
            "timestamp": datetime.utcnow().isoformat()
        }
    }

    return state
