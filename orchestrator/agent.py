from langgraph.graph import StateGraph, END
import uuid
from datetime import datetime

from orchestrator.state import TravelState
from orchestrator.extractor import extract_travel_details

from agents.flight_agent.agent import graph as flight_graph
from agents.hotel_agent.agent import graph as hotel_graph

def detect_intent(state: TravelState):

    text = state["user_input"].lower().strip()

    state["is_greeting"] = text in [
        "hi",
        "hello",
        "hey"
    ]

    state["is_modification_request"] = any(
        word in text
        for word in [
            "change",
            "modify",
            "update",
            "instead"
        ]
    )

    details = extract_travel_details(
        state["user_input"]
    )

    print("\nEXTRACTED =", details)

    existing = dict(
        state.get(
            "travel_parameters",
            {}
        )
    )

    print(
        "BEFORE MERGE =",
        existing
    )

    pending = state.get(
        "pending_clarification",
        []
    )

    # -------------------------
    # USER ANSWERING A QUESTION
    # -------------------------

    if pending:

        field = pending[0]

        if field == "origin":

            existing["origin"] = (
                state["user_input"]
                .strip()
                .title()
            )

        elif field == "destination":

            existing["destination"] = (
                state["user_input"]
                .strip()
                .title()
            )

        elif field == "departure_date":

            existing["departure_date"] = (
                details.get("departure_date")
                or state["user_input"]
            )

        elif field == "passengers":

            if text.isdigit():
                existing["passengers"] = int(text)

        elif field == "cabin_class":

            existing["cabin_class"] = (
                state["user_input"]
                .title()
            )

        elif field == "needs_hotel":

            if text == "yes":
                existing["needs_hotel"] = True

            elif text == "no":
                existing["needs_hotel"] = False

        elif field == "nights":

            import re

            match = re.search(
                r"(\d+)",
                text
            )

            if match:
                existing["nights"] = int(
                    match.group(1)
                )

        elif field == "hotel_location_preference":

            existing[
                "hotel_location_preference"
            ] = state["user_input"]

    else:

        print("DETAILS =", details)

        for key, value in details.items():

            if value in ["", None]:
                continue

            if key == "confidence":
                continue

            if key == "modification_request":
                continue

            if key == "needs_hotel":

                if existing.get("needs_hotel") is None:
                    existing["needs_hotel"] = value

                continue

            if key == "passengers" and value <= 0:
                continue

            if key == "nights" and value <= 0:
                continue

            existing[key] = value

            print(
                "AFTER MERGE =",
                existing
            )

            state["travel_parameters"] = existing

            print(
                "SAVED PARAMS =",
                state["travel_parameters"]
            )

    flight_keywords = [
        "flight",
        "fly",
        "airline",
        "ticket"
    ]

    hotel_keywords = [
        "hotel",
        "stay",
        "room",
        "resort"
    ]

    state["flight_required"] = (
        bool(existing.get("origin"))
        and
        bool(existing.get("destination"))
    )

    state["hotel_required"] = (
        existing.get(
            "needs_hotel",
            False
        )
    )

    state["is_general_question"] = any(
        word in text
        for word in [
            "weather",
            "best time",
            "safe",
            "culture",
            "food",
            "visit"
        ]
    )

    return state


def handle_greeting(state):


    if not state.get(
        "is_greeting",
        False
    ):
        return state

    state["final_response"] = """
    Hello! 👋

    I'm your Friendly Travel Assistant.

    I can help with:

    ✈️ Flights
    🏨 Hotels
    🌍 Travel Planning

    How can I help you today?
    """

    return state

def handle_general_question(state):
    print("GENERAL QUESTION NODE HIT")

    if not state.get(
        "is_general_question",
        False
    ):
        return state

    text = state["user_input"].lower()

    if "tokyo" in text:

        state["final_response"] = """
🌸 Tokyo is a wonderful destination year-round.

June offers:

• Pleasant temperatures
• Beautiful parks and gardens
• Fewer crowds than peak summer
• Great shopping and food experiences

Keep in mind that June is also part of Japan's rainy season, so carrying an umbrella is recommended.

Would you like help planning a trip to Tokyo?
"""
        return state

    if "paris" in text:

        state["final_response"] = """
🗼 Paris is especially beautiful during spring and early summer.

June offers:

• Comfortable weather
• Longer daylight hours
• Outdoor cafés and sightseeing
• Excellent photo opportunities

Would you like help booking flights or hotels for Paris?
"""
        return state

    state["final_response"] = """
🌍 I'd be happy to help with travel advice.

Please tell me the destination you're interested in and I'll provide some recommendations.
"""

    return state

def check_missing_information(state):

    if state.get("is_general_question", False):
        return state

    if state.get("is_greeting", False):
        return state

    params = state.get(
        "travel_parameters",
        {}
    )

    missing = []

    if not params.get("origin"):

        missing.append("origin")

    elif not params.get("destination"):

        missing.append("destination")

    elif not params.get("departure_date"):

        missing.append("departure_date")

    elif not params.get("passengers"):

        missing.append("passengers")

    elif not params.get("cabin_class"):

        missing.append("cabin_class")

    elif "needs_hotel" not in params:

        missing.append(
            "needs_hotel"
        )

    elif (
        params.get("needs_hotel") is True
        and
        not params.get("nights")
    ):

        missing.append("nights")

    elif (
        params.get("needs_hotel")
        and
        not params.get(
            "hotel_location_preference"
        )
    ):
        missing.append(
            "hotel_location_preference"
        )

    state["pending_clarification"] = []

    if missing:
        state["pending_clarification"] = missing

    return state


def ask_clarification(state):

    pending = state.get(
        "pending_clarification",
        []
    )

    if not pending:
        return state

    field = pending[0]

    if field == "origin":

        state["final_response"] = """
📍 Which city will you be departing from?

"""
        return state

    if field == "destination":

        state["final_response"] = """
🌍 What is your destination city?

"""
        return state

    if field == "departure_date":

        state["final_response"] = """
📅 When would you like to travel?

"""
        return state

    if field == "passengers":

        state["final_response"] = """
👥 How many travellers will be flying?
"""
        return state
    if field == "cabin_class":

        state["final_response"] = """
    💺 Which cabin class would you prefer?

    Options:

    • Economy
    • Premium Economy
    • Business
    • First
    """

        return state
    
    if field == "needs_hotel":

        state["final_response"] = """
    🏨 Will you also need a hotel?

    """

        return state
    
    if field == "hotel_location_preference":

        state["final_response"] = """
    📍 Any hotel location preference?

    """

        return state

    if field == "nights":

        state["final_response"] = """
    🌙 How many nights will you stay?

    """
        return state

def handle_modification(state):

    if not state.get(
        "is_modification_request",
        False
    ):
        return state

    params = state.get(
        "travel_parameters",
        {}
    )

    # ----------------------------------
    # RESET OLD SEARCH RESULTS
    # ----------------------------------

    if params.get("destination"):

        state["selected_flight"] = None

        state["selected_hotel"] = None

        state["flight_response"] = {}

        state["hotel_response"] = {}

        state["awaiting_flight_selection"] = False

        state["awaiting_flight_confirmation"] = False

        state["awaiting_hotel_selection"] = False

        state["awaiting_hotel_confirmation"] = False

        state["awaiting_hotel_opt_in"] = False

        state["booking_confirmed"] = False

    # ----------------------------------
    # BUILD FRIENDLY RESPONSE
    # ----------------------------------

    response = """
Sure 😊

I've updated your trip details.
"""

    if params.get("origin"):

        response += (
            f"\n📍 Origin: "
            f"{params['origin']}"
        )

    if params.get("destination"):

        response += (
            f"\n📍 Destination: "
            f"{params['destination']}"
        )

    if params.get("departure_date"):

        response += (
            f"\n📅 Date: "
            f"{params['departure_date']}"
        )

    if params.get("passengers"):

        response += (
            f"\n👥 Passengers: "
            f"{params['passengers']}"
        )

    if params.get("cabin_class"):

        response += (
            f"\n💺 Cabin: "
            f"{params['cabin_class']}"
        )

    response += """

🔄 Searching again with your updated preferences...
"""

    state["final_response"] = response

    return state

def call_flight_agent(state):

    if state.get(
        "pending_clarification",
        []
    ):
        return state

    params = state["travel_parameters"]

    request = {
        "task_id": str(uuid.uuid4()),
        "task_type": "flight_search",
        "session_id": str(uuid.uuid4()),

        "parameters": {
            "origin": params.get(
                "origin",
                ""
            ),

            "destination": params.get(
                "destination",
                ""
            ),

            "departure_date": params.get(
                "departure_date",
                ""
            ),

            "return_date": params.get(
                "return_date",
                ""
            ),

            "passengers": params.get(
                "passengers",
                1
            ),

            "cabin_class": params.get(
                "cabin_class",
                "economy"
            )
        },

        "metadata": {
            "requested_by": "orchestrator",
            "timestamp": datetime.utcnow().isoformat()
        }
    }

    result = flight_graph.invoke(
        {
            "request": request
        }
    )

    state["flight_response"] = (
        result.get(
            "response",
            {}
        )
    )

    return state


def call_hotel_agent(state):

    if state.get(
        "pending_clarification",
        []
    ):
        return state

    params = state["travel_parameters"]

    request = {
        "task_id": str(uuid.uuid4()),
        "task_type": "hotel_search",
        "session_id": str(uuid.uuid4()),

        "parameters": {
            "destination": params.get(
                "destination",
                ""
            ),

            "check_in_date": params.get(
                "departure_date",
                ""
            ),

            "check_out_date": params.get(
                "return_date",
                ""
            ),

            "guests": params.get(
                "passengers",
                1
            ),

            "hotel_location_preference": params.get(
                "hotel_location_preference",
                ""
            )
        },

        "metadata": {
            "requested_by": "orchestrator",
            "timestamp": datetime.utcnow().isoformat()
        }
    }

    result = hotel_graph.invoke(
        {
            "request": request
        }
    )

    state["hotel_response"] = (
        result.get(
            "response",
            {}
        )
    )

    return state


def route_after_modification(state):

    if state.get(
        "is_general_question",
        False
    ):
        return "end"

    if state.get(
        "pending_clarification",
        []
    ):
        return "end"

    flight_needed = state.get(
        "flight_required",
        False
    )

    hotel_needed = state.get(
        "hotel_required",
        False
    )

    if flight_needed:
        return "flight_agent"

    if hotel_needed:
        return "hotel_agent"

    return "aggregate"

def finish_response(state):
    return state

def route_after_flight(state):

    if state.get(
        "hotel_required",
        False
    ):
        return "hotel_agent"

    return "aggregate"

def handle_flight_selection(state):

    text = state["user_input"].lower()

    if not state.get(
        "awaiting_flight_selection",
        False
    ):
        return state

    flights = state.get(
        "flight_response",
        {}
    ).get(
        "results",
        []
    )

    if not flights:
        return state

    selected = None

    if "1" in text:
        selected = flights[0]

    elif "2" in text and len(flights) > 1:
        selected = flights[1]

    else:

        for flight in flights:

            if (
                flight["airline"]
                .lower()
                in text
            ):
                selected = flight
                break

    if not selected:
        return state

    state["selected_flight"] = selected

    state[
        "awaiting_flight_selection"
    ] = False

    state[
        "awaiting_flight_confirmation"
    ] = True

    params = state.get(
        "travel_parameters",
        {}
    )
    print("TRAVEL PARAMS =", params)

    state["final_response"] = f"""
    📋 Trip Review

    📍 Origin
    {params.get('origin')}

    📍 Destination
    {params.get('destination')}

    📅 Departure Date
    {params.get('departure_date')}

    👥 Passengers
    {params.get('passengers')}

    💺 Cabin Class
    {params.get('cabin_class')}

    ✈️ Selected Flight
    {selected['airline']}
    ({selected['flight_number']})

    💰 Flight Price
    ${selected['price']}

    Please review the details above.

    Would you like to confirm this flight?

    """

    return state

def confirm_flight(state):

    print("\n====================")
    print("CONFIRM FLIGHT CALLED")
    print(state)
    print("====================\n")

    text = state["user_input"].lower()

    if not state.get(
        "awaiting_flight_confirmation",
        False
    ):
        return state

    if text not in [
        "yes",
        "confirm",
        "ok"
    ]:
        return state

    state[
        "awaiting_flight_confirmation"
    ] = False

    state[
        "awaiting_hotel_selection"
    ] = False
    hotels = (
        state.get(
            "hotel_response",
            {}
        ).get(
            "results",
            []
        )
    )

    # ----------------------------------
    # NO HOTELS AVAILABLE
    # ----------------------------------

    if not hotels:

        state["awaiting_hotel_opt_in"] = True

        state["final_response"] = f"""
    ✈️ Flight Confirmed

    Airline:
    {state['selected_flight']['airline']}

    Flight:
    {state['selected_flight']['flight_number']}

    Price:
    ${state['selected_flight']['price']}

    Would you also like me to find a hotel?

    """

        return state

    # Hotel list exists
    # Ask user if they want hotel first

    state["awaiting_hotel_opt_in"] = True

    state["final_response"] = f"""
    ✈️ Flight Confirmed

    Airline:
    {state['selected_flight']['airline']}

    Flight:
    {state['selected_flight']['flight_number']}

    Price:
    ${state['selected_flight']['price']}

    Would you also like me to find a hotel?
    """

    return state

def handle_hotel_selection(state):

    text = state["user_input"].lower()

    if not state.get(
        "awaiting_hotel_selection",
        False
    ):
        return state

    hotels = state.get(
        "hotel_response",
        {}
    ).get(
        "results",
        []
    )

    if not hotels:

        state["final_response"] = (
            "Sorry, I couldn't find any hotels."
        )

        state["awaiting_hotel_selection"] = False

        return state

    selected = None

    if text.isdigit():

        idx = int(text) - 1

        if 0 <= idx < len(hotels):
            selected = hotels[idx]

    else:

        for hotel in hotels:

            if (
                hotel["name"]
                .lower()
                in text
            ):
                selected = hotel
                break

    if not selected:
        return state

    state["selected_hotel"] = selected

    state[
        "awaiting_hotel_selection"
    ] = False

    state[
        "awaiting_hotel_confirmation"
    ] = True

    state["final_response"] = f"""
    🏨 Hotel Review

    Hotel:
    {selected['name']}

    ⭐ Stars:
    {selected['stars']}

    💰 Price:
    ${selected['price_per_night']}/night

    🎁 Amenities:
    {", ".join(selected.get("amenities", []))}

    📍 Distance:
    {selected.get("distance", "N/A")}

    Please review the hotel details.

    Would you like to confirm this hotel?

    """

    return state

def confirm_hotel(state):

    text = state["user_input"].lower()

    if not state.get(
        "awaiting_hotel_confirmation",
        False
    ):
        return state

    if text not in [
        "yes",
        "confirm",
        "ok"
    ]:
        return state

    # ----------------------------
    # COMPLETE BOOKING
    # ----------------------------

    state[
        "awaiting_hotel_confirmation"
    ] = False

    state["booking_confirmed"] = True

    # ----------------------------
    # RESET CONVERSATION FLAGS
    # ----------------------------

    state["awaiting_flight_selection"] = False

    state["awaiting_flight_confirmation"] = False

    state["awaiting_hotel_selection"] = False

    state["awaiting_hotel_confirmation"] = False

    state["awaiting_hotel_opt_in"] = False

    # ----------------------------
    # GET SELECTED ITEMS
    # ----------------------------

    flight = state.get(
        "selected_flight",
        {}
    )

    hotel = state.get(
        "selected_hotel",
        {}
    )

    params = state.get(
        "travel_parameters",
        {}
    )

    # ----------------------------
    # FINAL RESPONSE
    # ----------------------------

    state["final_response"] = f"""
    🎉 Booking Confirmed

    ━━━━━━━━━━━━━━━━━━━━

    ✈️ Flight

    Airline:
    {flight.get('airline')}

    Flight Number:
    {flight.get('flight_number')}

    Price:
    ${flight.get('price')}

    ━━━━━━━━━━━━━━━━━━━━

    🏨 Hotel

    {hotel.get('name')}

    Price:
    ${hotel.get('price_per_night')}/night

    ━━━━━━━━━━━━━━━━━━━━

    📍 Origin
    {params.get('origin')}

    📍 Destination
    {params.get('destination')}

    📅 Departure Date
    {params.get('departure_date')}

    📅 Return Date
    {params.get('return_date', 'One Way')}

    👥 Passengers
    {params.get('passengers')}

    💺 Cabin Class
    {params.get('cabin_class')}

    📍 Hotel Preference
    {params.get('hotel_location_preference', 'No preference')}

    ━━━━━━━━━━━━━━━━━━━━

    Thank you for using Friendly Travel Assistant.
    """
    return state


def aggregate_results(state):

    # DO NOT overwrite greeting response

    if state.get("is_greeting", False):
        return state

    if state.get(
        "pending_clarification",
        []
    ):
        return state

    params = state.get(
        "travel_parameters",
        {}
    )

    response = f"""
    ✈️ Trip Search Results

    Origin:
    {params.get('origin','')}

    Destination:
    {params.get('destination','')}

    Departure:
    {params.get('departure_date','')}

    Travellers:
    {params.get('passengers',1)}

    Cabin:
    {params.get('cabin_class','economy')}
    """

    flight_response = state.get(
        "flight_response",
        {}
    )

    if (
        flight_response.get("status")
        == "success"
    ):

        response += "\n\n✈️ Available Flights\n"

        for idx, flight in enumerate(
            flight_response.get(
                "results",
                []
            ),
            start=1
        ):

            response += f"""

    {idx}. {flight['airline']}
    Flight: {flight['flight_number']}
    Departure: {flight['departure']}
    Arrival: {flight['arrival']}
    Price: ${flight['price']}
    """

        # ----------------------------------
        # WAIT FOR USER TO PICK FLIGHT
        # ----------------------------------

        state["awaiting_flight_selection"] = True

        response += """

        Please choose a flight.
        """
    else:

        response += """

        ❌ Sorry, I couldn't find flights for that route.

        You may try:

        • Tokyo
        • Paris
        • Singaporeund.
        """

    state["final_response"] = response

    return state


builder = StateGraph(
    TravelState
)

builder.add_node(
"detect_intent",
detect_intent
)

builder.add_node(
"greeting",
handle_greeting
)

builder.add_node(
    "general_question",
    handle_general_question
)

builder.add_node(
"check_missing",
check_missing_information
)

builder.add_node(
"clarification",
ask_clarification
)

builder.add_node(
"modification",
handle_modification
)

builder.add_node(
"flight_agent",
call_flight_agent
)

builder.add_node(
"hotel_agent",
call_hotel_agent
)

builder.add_node(
"flight_selection",
handle_flight_selection
)

builder.add_node(
"flight_confirmation",
confirm_flight
)

builder.add_node(
"hotel_selection",
handle_hotel_selection
)

builder.add_node(
"hotel_confirmation",
confirm_hotel
)

builder.add_node(
"aggregate",
aggregate_results
)

builder.add_node(
    "end",
    finish_response
)

builder.set_entry_point(
"detect_intent"
)

builder.add_edge(

"detect_intent",
"greeting"
)

builder.add_edge(
    "greeting",
    "general_question"
)

builder.add_edge(
    "general_question",
    "check_missing"
)

builder.add_edge(
"check_missing",
"clarification"
)

builder.add_edge(
"clarification",
"modification"
)

builder.add_conditional_edges(
    "modification",
    route_after_modification,
    {
        "flight_agent": "flight_agent",
        "hotel_agent": "hotel_agent",
        "aggregate": "aggregate",
        "end": "end"
    }
)

builder.add_conditional_edges(
    "flight_agent",
    route_after_flight,
    {
        "hotel_agent": "hotel_agent",
        "aggregate": "aggregate"
    }
)

builder.add_edge(
    "hotel_agent",
    "aggregate"
)

builder.add_edge(
    "end",
    "__end__"
)

graph = builder.compile()
