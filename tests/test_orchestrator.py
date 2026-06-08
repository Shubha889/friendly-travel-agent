import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from orchestrator.agent import graph


def test_orchestrator():

    result = graph.invoke(
        {
            "user_input":
            "I want to fly from Singapore to Tokyo on June 15 and need a hotel"
        }
    )

    print(result["final_response"])

def test_general_question():

    from orchestrator.agent import graph

    result = graph.invoke(
        {
            "user_input":
                "Is June a good time to visit Tokyo?"
        }
    )

    assert (
        "Tokyo"
        in result["final_response"]
    )

    print(result["final_response"])