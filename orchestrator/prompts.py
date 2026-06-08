CONFIRM_TRAVEL_DETAILS = """
That sounds like an exciting trip! 😊

Let me confirm the details:

📍 Origin: {origin}
📍 Destination: {destination}
📅 Departure Date: {departure_date}

Would you like me to search for available flight options?
"""

FLIGHT_SELECTION_PROMPT = """
Great! Let me check available flights for you. ✈️

I found these options:

{flight_options}

Which flight would you like to select?
"""

FLIGHT_CONFIRMATION_PROMPT = """
Excellent choice! ✈️

You selected:

{flight_details}

Would you like me to proceed with this flight booking?
"""

HOTEL_SELECTION_PROMPT = """
Your flight selection has been confirmed.

Now let's find a hotel in {destination}. 🏨

{hotel_options}

Which hotel would you like to select?
"""

HOTEL_CONFIRMATION_PROMPT = """
Great choice! 🏨

You selected:

{hotel_details}

Would you like me to proceed with this hotel booking?
"""

BOOKING_SUMMARY_PROMPT = """
🎉 Booking Summary

Flight:
{flight_name}

Hotel:
{hotel_name}

Destination:
{destination}

Travel Date:
{departure_date}

Thank you for using Friendly Travel Assistant!
"""