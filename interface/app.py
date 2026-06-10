import streamlit as st
import sys
import os
import traceback

print("APP LOADED")

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from orchestrator.agent import (
    graph,
    handle_flight_selection,
    confirm_flight,
    handle_hotel_selection,
    confirm_hotel
)

st.set_page_config(
    page_title="Friendly Travel Assistant",
    page_icon="✈️"
)

st.title("✈️ Friendly Travel Assistant")

# ==================================================
# SESSION STATE
# ==================================================

defaults = {
    "messages": [],
    "travel_parameters": {},
    "pending_clarification": [],
    "stage": "collect_details",
    "flight_response": {},
    "hotel_response": {},
    "selected_flight": None,
    "selected_hotel": None,
    "awaiting_flight_selection": False,
    "awaiting_flight_confirmation": False,
    "awaiting_hotel_opt_in": False,
    "awaiting_hotel_selection": False,
    "awaiting_hotel_confirmation": False,
    "booking_confirmed": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# params.get("needs_hotel") is None
def reset_trip_state():

    st.session_state.travel_parameters = {}
    
    st.session_state.pending_clarification = []

    st.session_state.flight_response = {}

    st.session_state.hotel_response = {}

    st.session_state.selected_flight = None

    st.session_state.selected_hotel = None

    st.session_state.awaiting_flight_selection = False

    st.session_state.awaiting_flight_confirmation = False

    st.session_state.awaiting_hotel_opt_in = False

    st.session_state.awaiting_hotel_selection = False

    st.session_state.awaiting_hotel_confirmation = False

    st.session_state.booking_confirmed = False

# ==================================================
# CHAT HISTORY
# ==================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ==================================================
# USER INPUT
# ==================================================

user_input = st.chat_input(
    "Where would you like to travel?"
)

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    new_trip_keywords = [
        "travel from",
        "fly from",
        "book a trip",
        "trip from",
        "i want to travel"
    ]

    if any(
        keyword in user_input.lower()
        for keyword in new_trip_keywords
    ):
        reset_trip_state()
    
    # if st.session_state.booking_confirmed:
    #     reset_trip_state()
    #     st.session_state.booking_confirmed = False   

    try:

        # ----------------------------------
        # FLIGHT SELECTION
        # ----------------------------------

        if st.session_state.awaiting_flight_selection:

            state = {
                "user_input": user_input,

                "flight_response":
                    st.session_state.flight_response,

                "travel_parameters":
                    st.session_state.travel_parameters,

                "awaiting_flight_selection":
                    True
            }

            result = handle_flight_selection(
                state
            )
            st.session_state.selected_flight = result.get(
                "selected_flight"
            )

            st.session_state.awaiting_flight_selection = False

            st.session_state.awaiting_flight_confirmation = True

            response = result["final_response"]

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            st.rerun()
            st.stop()

            print("FLIGHT_SELECTION_RESULT =", result)

        # ----------------------------------
        # FLIGHT CONFIRMATION
        # ----------------------------------

        elif st.session_state.awaiting_flight_confirmation:

            modification_words = [
                "change",
                "modify",
                "update",
                "instead",
                "destination",
                "origin"
            ]

            if any(
                word in user_input.lower()
                for word in modification_words
            ):

                st.session_state.awaiting_flight_confirmation = False
                st.session_state.awaiting_flight_selection = False

                result = graph.invoke(
                    {
                        "user_input": user_input,

                        "conversation_history":
                            st.session_state.messages,

                        "travel_parameters":
                            st.session_state.travel_parameters,

                        "stage":
                            st.session_state.stage,

                        "flight_response": {},

                        "hotel_response": {},

                        "selected_flight":
                            st.session_state.selected_flight,

                        "selected_hotel":
                            st.session_state.selected_hotel,

                        "awaiting_flight_selection": False,

                        "awaiting_flight_confirmation": False,

                        "awaiting_hotel_selection": False,

                        "awaiting_hotel_confirmation": False,

                        "booking_confirmed": False,

                        "pending_clarification":
                            st.session_state.pending_clarification,

                        "flight_required": False,

                        "hotel_required": False,

                        "is_greeting": False,

                        "is_general_question": False,

                        "is_modification_request": False,

                        "final_response": ""
                    }
                )

            else:

                print("APP -> FLIGHT CONFIRMATION")

                state = {
                    "user_input": user_input,

                    "hotel_response":
                        st.session_state.hotel_response,

                    "awaiting_flight_confirmation":
                        True,

                    "selected_flight":
                        st.session_state.selected_flight
                }

                result = confirm_flight(state)
                print("RESULT =", result)

                # FORCE SAVE IMMEDIATELY

                st.session_state.awaiting_flight_confirmation = (
                    result.get(
                        "awaiting_flight_confirmation",
                        False
                    )
                )

                st.session_state.awaiting_hotel_opt_in = (
                    result.get(
                        "awaiting_hotel_opt_in",
                        False
                    )
                )

                st.session_state.awaiting_hotel_selection = (
                    result.get(
                        "awaiting_hotel_selection",
                        False
                    )
                )

                st.session_state.selected_flight = (
                    result.get(
                        "selected_flight",
                        st.session_state.selected_flight
                    )
                )

                if result.get("awaiting_hotel_opt_in"):
                    st.session_state.awaiting_hotel_opt_in = True

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["final_response"]
                    }
                )

                st.rerun()
                st.stop()

        # ----------------------------------
        # PRIORITY 1: HOTEL NIGHTS (if opted in)
        # ----------------------------------
        elif (
            st.session_state.awaiting_hotel_opt_in
            and user_input.lower().strip()
            in ["yes", "y", "ok", "sure"]
        ):

            st.session_state.awaiting_hotel_opt_in = False

            params = st.session_state.travel_parameters

            if not params.get("nights"):
                params["nights"] = 5

            from agents.hotel_agent.agent import (
                graph as hotel_graph
            )

            hotel_result = hotel_graph.invoke(
                {
                    "request": {
                        "task_id": "hotel-search",
                        "task_type": "hotel_search",
                        "session_id": "session-1",
                        "parameters": {
                            "destination":
                                params.get("destination", ""),

                            "check_in_date":
                                params.get("departure_date", ""),

                            "guests":
                                params.get("passengers", 1),

                            "hotel_location_preference":
                                params.get(
                                    "hotel_location_preference",
                                    ""
                                )
                        },
                        "metadata": {}
                    }
                }
            )

            st.session_state.hotel_response = (
                hotel_result.get(
                    "response",
                    {}
                )
            )

            hotels = (
                st.session_state.hotel_response
                .get("results", [])
            )

            if not hotels:

                response = """
            🏨 Sorry, I couldn't find hotels for this destination.
            """

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

                st.rerun()
                st.stop()

            st.session_state.awaiting_hotel_selection = True

            response = "🏨 Available Hotels\n\n"

            for idx, hotel in enumerate(
                hotels,
                start=1
            ):

                response += f"""
        {idx}. {hotel['name']}
        ⭐ {hotel['stars']}
        💰 ${hotel['price_per_night']}/night
        📍 {hotel.get('distance','N/A')}

        """

            response += "\nPlease choose a hotel."

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            st.rerun()
            st.stop()
       
        elif st.session_state.awaiting_hotel_selection:

            state = {
                "user_input": user_input,

                "hotel_response":
                    st.session_state.hotel_response,

                "awaiting_hotel_selection":
                    True
            }

            result = handle_hotel_selection(
                state
            )

            st.session_state.selected_hotel = (
                result.get(
                    "selected_hotel"
                )
            )

            st.session_state.awaiting_hotel_selection = False

            st.session_state.awaiting_hotel_confirmation = True

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": result["final_response"]
                }
            )

            st.rerun()
            st.stop()
        # ----------------------------------
        # HOTEL CONFIRMATION
        # ----------------------------------

        elif st.session_state.awaiting_hotel_confirmation:

            modification_words = [
                "change",
                "modify",
                "update",
                "instead",
                "destination",
                "hotel"
            ]

            if any(
                word in user_input.lower()
                for word in modification_words
            ):

                st.session_state.awaiting_hotel_confirmation = False
                st.session_state.awaiting_hotel_selection = False

                result = graph.invoke(
                    {
                        "user_input": user_input,

                        "conversation_history":
                            st.session_state.messages,

                        "travel_parameters":
                            st.session_state.travel_parameters,

                        "stage":
                            st.session_state.stage,

                        "flight_response": {},

                        "hotel_response": {},

                        "selected_flight":
                            st.session_state.selected_flight,

                        "selected_hotel":
                            st.session_state.selected_hotel,

                        "awaiting_flight_selection": False,

                        "awaiting_flight_confirmation": False,

                        "awaiting_hotel_selection": False,

                        "awaiting_hotel_confirmation": False,

                        "booking_confirmed": False,

                        "pending_clarification":
                            st.session_state.pending_clarification,

                        "flight_required": False,

                        "hotel_required": False,

                        "is_greeting": False,

                        "is_general_question": False,

                        "is_modification_request": False,

                        "final_response": ""
                    }
                )

            else:

                state = {
                    "user_input": user_input,
                    "selected_flight":
                        st.session_state.selected_flight,
                    "selected_hotel":
                        st.session_state.selected_hotel,
                    "travel_parameters":
                        st.session_state.travel_parameters,
                    "awaiting_hotel_confirmation":
                        True
                }

                result = confirm_hotel(state)

                st.session_state.booking_confirmed = (
                    result.get(
                        "booking_confirmed",
                        False
                    )
                )

                st.session_state.awaiting_hotel_confirmation = (
                    result.get(
                        "awaiting_hotel_confirmation",
                        False
                    )
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["final_response"]
                    }
                )

                st.rerun()
                st.stop()

        elif (
            st.session_state.awaiting_hotel_opt_in
            and user_input.lower().strip()
            in ["no", "nope", "not", "skip"]
        ):

            st.session_state.awaiting_flight_selection = False
            st.session_state.awaiting_flight_confirmation = False
            st.session_state.awaiting_hotel_selection = False
            st.session_state.awaiting_hotel_confirmation = False
            st.session_state.awaiting_hotel_opt_in = False

            st.session_state.booking_confirmed = True

            flight = st.session_state.selected_flight
            params = st.session_state.travel_parameters

            response = f"""
            ✅ Flight Booking Confirmed

            ━━━━━━━━━━━━━━━━━━━━

            ✈️ Flight

            Airline: {flight.get('airline')}
            Flight Number: {flight.get('flight_number')}
            Price: ${flight.get('price')}

            ━━━━━━━━━━━━━━━━━━━━

            📍 Origin: {params.get('origin')}
            📍 Destination: {params.get('destination')}
            📅 Departure Date: {params.get('departure_date')}
            👥 Passengers: {params.get('passengers')}
            💺 Cabin: {params.get('cabin_class', 'Economy')}

            ━━━━━━━━━━━━━━━━━━━━

            Thank you for using Friendly Travel Assistant!
            """

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            st.rerun()
            st.stop()
        # ----------------------------------
        # NORMAL ORCHESTRATOR
        # ----------------------------------

        else:

            # ----------------------------------
            # NEEDS HOTEL ANSWER
            # ----------------------------------

            if (
                st.session_state.pending_clarification
                and
                st.session_state.pending_clarification[0]
                == "needs_hotel"
            ):

                if user_input.lower() == "yes":

                    st.session_state.travel_parameters[
                        "needs_hotel"
                    ] = True

                    if (
                        st.session_state.pending_clarification
                        and
                        st.session_state.pending_clarification[0]
                        == "needs_hotel"
                    ):
                        st.session_state.pending_clarification = []

                elif user_input.lower() == "no":

                    st.session_state.travel_parameters[
                        "needs_hotel"
                    ] = False

            # ----------------------------------
            # NIGHTS ANSWER
            # ----------------------------------

            elif (
                st.session_state.pending_clarification
                and
                st.session_state.pending_clarification[0]
                == "nights"
                and
                user_input.isdigit()
            ):

                st.session_state.travel_parameters[
                    "nights"
                ] = int(user_input)

            result = graph.invoke(
                {
                    "user_input": user_input,

                    "conversation_history":
                        st.session_state.messages,

                    "travel_parameters":
                        st.session_state.travel_parameters,

                    "stage":
                        st.session_state.stage,

                    "flight_response":
                        st.session_state.flight_response,

                    "hotel_response":
                        st.session_state.hotel_response,

                    "selected_flight":
                        st.session_state.selected_flight,

                    "selected_hotel":
                        st.session_state.selected_hotel,

                    "awaiting_flight_selection":
                        st.session_state.awaiting_flight_selection,

                    "awaiting_flight_confirmation":
                        st.session_state.awaiting_flight_confirmation,

                    "awaiting_hotel_selection":
                        st.session_state.awaiting_hotel_selection,

                    "awaiting_hotel_confirmation":
                        st.session_state.awaiting_hotel_confirmation,

                    "booking_confirmed":
                        st.session_state.booking_confirmed,

                    "pending_clarification":
                        st.session_state.pending_clarification,

                    "flight_required": False,

                    "hotel_required": False,

                    "is_greeting": False,

                    "is_general_question": False,

                    "is_modification_request": False,

                    "final_response": ""
                }
            )

        # ----------------------------------
        # SAVE MEMORY
        # ----------------------------------

        if result.get("travel_parameters"):

            st.session_state.travel_parameters.update(
                result["travel_parameters"]
            )

        st.session_state.flight_response = (
            result.get(
                "flight_response",
                st.session_state.flight_response
            )
        )

        st.session_state.hotel_response = (
            result.get(
                "hotel_response",
                st.session_state.hotel_response
            )
        )

        st.session_state.selected_flight = (
            result.get(
                "selected_flight",
                st.session_state.selected_flight
            )
        )

        st.session_state.selected_hotel = (
            result.get(
                "selected_hotel",
                st.session_state.selected_hotel
            )
        )

        st.session_state.awaiting_flight_selection = (
            result.get(
                "awaiting_flight_selection",
                st.session_state.awaiting_flight_selection
            )
        )

        st.session_state.awaiting_flight_confirmation = (
            result.get(
                "awaiting_flight_confirmation",
                st.session_state.awaiting_flight_confirmation
            )
        )
        print(
            "SESSION AFTER SAVE",
            st.session_state.awaiting_flight_selection,
            st.session_state.awaiting_flight_confirmation
        )

        st.session_state.awaiting_hotel_opt_in = (
            result.get(
                "awaiting_hotel_opt_in",
                st.session_state.awaiting_hotel_opt_in
            )
        )

        st.session_state.awaiting_hotel_selection = (
            result.get(
                "awaiting_hotel_selection",
                st.session_state.awaiting_hotel_selection
            )
        )

        st.session_state.awaiting_hotel_confirmation = (
            result.get(
                "awaiting_hotel_confirmation",
                st.session_state.awaiting_hotel_confirmation
            )
        )

        st.session_state.booking_confirmed = (
            result.get(
                "booking_confirmed",
                st.session_state.booking_confirmed
            )
        )

        if result.get(
            "travel_parameters"
        ):

            st.session_state.travel_parameters.update(
                result["travel_parameters"]
            )
        print(
            "SAVE FLAGS",
            result.get("awaiting_flight_selection"),
            result.get("awaiting_flight_confirmation")
        )

        print(
            "SESSION BEFORE SAVE",
            st.session_state.awaiting_flight_selection,
            st.session_state.awaiting_flight_confirmation
        )    

        response = result.get(
            "final_response",
            "Sorry, I couldn't process your request."
        )

    except Exception as e:

        traceback.print_exc()

        response = (
            f"⚠️ System Error:\n\n{str(e)}"
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
 
    with st.chat_message("assistant"):
        st.write(response)