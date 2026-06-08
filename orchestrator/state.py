from typing import TypedDict


class TravelState(TypedDict):

    # ---------------------------------
    # USER INPUT
    # ---------------------------------

    user_input: str

    # ---------------------------------
    # CONVERSATION MEMORY
    # ---------------------------------

    conversation_history: list

    # ---------------------------------
    # EXTRACTED TRAVEL DETAILS
    # ---------------------------------

    travel_parameters: dict

    # Example:
    # {
    #   origin,
    #   destination,
    #   departure_date,
    #   return_date,
    #   passengers,
    #   cabin_class,
    #   needs_hotel,
    #   nights,
    #   hotel_location_preference
    # }

    # ---------------------------------
    # MISSING INFORMATION
    # ---------------------------------

    pending_clarification: list

    # ---------------------------------
    # CURRENT STAGE
    # ---------------------------------

    stage: str

    # collect_details
    # awaiting_flight_selection
    # flight_selected
    # awaiting_flight_confirmation
    # awaiting_hotel_selection
    # hotel_selected
    # awaiting_hotel_confirmation
    # awaiting_modification
    # booking_completed

    # ---------------------------------
    # INTENT FLAGS
    # ---------------------------------

    is_greeting: bool

    is_general_question: bool

    is_modification_request: bool

    # ---------------------------------
    # TRAVEL REQUIREMENTS
    # ---------------------------------

    flight_required: bool

    hotel_required: bool

    # ---------------------------------
    # PASSENGER DETAILS
    # ---------------------------------

    passengers: int

    cabin_class: str

    # economy
    # premium economy
    # business
    # first

    # ---------------------------------
    # DATE DETAILS
    # ---------------------------------

    departure_date: str

    return_date: str

    nights: int

    # ---------------------------------
    # HOTEL PREFERENCE
    # ---------------------------------

    hotel_location_preference: str

    # Example:
    # Shinjuku
    # Eiffel Tower
    # Marina Bay

    # ---------------------------------
    # FLIGHT AGENT
    # ---------------------------------

    flight_response: dict

    selected_flight: dict | None

    awaiting_flight_selection: bool

    awaiting_flight_confirmation: bool

    # ---------------------------------
    # HOTEL AGENT
    # ---------------------------------

    hotel_response: dict

    selected_hotel: dict | None

    awaiting_hotel_selection: bool

    awaiting_hotel_confirmation: bool

    awaiting_hotel_opt_in: bool

    # ---------------------------------
    # BOOKING STATUS
    # ---------------------------------

    booking_confirmed: bool

    # ---------------------------------
    # MODIFICATIONS
    # ---------------------------------

    pending_modification: dict

    # Example:
    # {
    #   "destination": "Paris"
    # }

    # ---------------------------------
    # FINAL RESPONSE
    # ---------------------------------

    final_response: str