from typing import TypedDict
from .mock_data import MOCK_FLIGHTS
from datetime import datetime

class FlightState(TypedDict):
    request: dict
    flights: list
    response: dict


def validate_input(state: FlightState):

    request = state["request"]

    params = request["parameters"]

    required = [
        "origin",
        "destination",
        "departure_date"
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


def search_flights(state: FlightState):

    if state.get("response"):
        return state

    params = state["request"]["parameters"]

    origin = (
        params.get(
            "origin",
            ""
        )
        .strip()
        .title()
    )

    destination = (
        params.get(
            "destination",
            ""
        )
        .strip()
        .title()
    )

    results = MOCK_FLIGHTS.get(
        (
            origin,
            destination
        ),
        []
    )

    results = sorted(
        results,
        key=lambda x: x["price"]
    )

    state["flights"] = results

    return state

def format_response(state: FlightState):

    if state.get("response"):
        return state

    flights = state.get(
        "flights",
        []
    )

    if not flights:

        state["response"] = {
            "task_id": state["request"].get(
                "task_id",
                "flight-task"
            ),
            "status": "failed",
            "results": [],
            "clarification_needed": None,
            "error": "No flights available",
            "metadata": {
                "agent_id": "flight-agent",
                "timestamp": datetime.utcnow().isoformat()
            }
        }

        return state

    state["response"] = {
        "task_id": state["request"].get(
            "task_id",
            "flight-task"
        ),
        "status": "success",
        "results": flights,
        "clarification_needed": None,
        "error": None,
        "metadata": {
            "agent_id": "flight-agent",
            "timestamp": datetime.utcnow().isoformat()
        }
    }

    return state