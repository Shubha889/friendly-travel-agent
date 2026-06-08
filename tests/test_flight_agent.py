import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from agents.flight_agent.agent import graph


def test_flight_agent():

    state = {
        "request": {
            "parameters": {
                "origin": "Singapore",
                "destination": "Tokyo",
                "departure_date": "2026-06-15"
            }
        }
    }

    result = graph.invoke(state)

    print(result)