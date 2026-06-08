import json
import re

from datetime import datetime
from datetime import timedelta

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)


def default_response():

    return {
        "origin": "",
        "destination": "",
        "departure_date": "",
        "return_date": "",
        "passengers": 0,
        "cabin_class": "",
        "needs_hotel": False,
        "nights": 0,
        "hotel_location_preference": "",
        "modification_request": False,
        "confidence": "low"
    }


def normalize_date(text):

    text = text.lower().strip()

    today = datetime.now()

    # -----------------------------
    # RELATIVE DATES
    # -----------------------------

    if text == "today":

        return today.strftime(
            "%Y-%m-%d"
        )

    if text == "tomorrow":

        return (
            today + timedelta(days=1)
        ).strftime("%Y-%m-%d")

    if text in [
        "day after",
        "day after tomorrow"
    ]:

        return (
            today + timedelta(days=2)
        ).strftime("%Y-%m-%d")

    # -----------------------------
    # NEXT FRIDAY
    # -----------------------------

    if text == "next friday":

        days = (4 - today.weekday()) % 7

        if days == 0:
            days = 7

        return (
            today + timedelta(days=days)
        ).strftime("%Y-%m-%d")

    # -----------------------------
    # NEXT MONDAY
    # -----------------------------

    if text == "next monday":

        days = (0 - today.weekday()) % 7

        if days == 0:
            days = 7

        return (
            today + timedelta(days=days)
        ).strftime("%Y-%m-%d")

    # -----------------------------
    # 19 June
    # 19th June
    # 19 Jun
    # 19th Jun
    # -----------------------------

    date_match = re.search(
        r"(\d{1,2})(st|nd|rd|th)?\s+([a-zA-Z]+)",
        text
    )

    if date_match:

        day = int(
            date_match.group(1)
        )

        month = (
            date_match.group(3)
            .capitalize()
        )

        current_year = today.year

        # Try full month name first
        try:

            parsed = datetime.strptime(
                f"{day} {month}",
                "%d %B"
            )

        except:

            try:

                parsed = datetime.strptime(
                    f"{day} {month}",
                    "%d %b"
                )

            except:

                return text

        parsed = parsed.replace(
            year=today.year
        )

        # If date already passed this year,
        # move to next year

        if parsed.date() < today.date():

            parsed = parsed.replace(
                year=today.year + 1
            )

        return parsed.strftime(
            "%Y-%m-%d"
        )

    return text


def extract_travel_details(
    user_input: str
):

    text = user_input.lower().strip()

    result = default_response()

    # -----------------------------
    # PASSENGERS
    # -----------------------------

    passenger_match = re.search(
        r"(\d+)\s+(passenger|traveller|traveler|people|guests)",
        text
    )

    if passenger_match:

        result["passengers"] = int(
            passenger_match.group(1)
        )

        result["confidence"] = "high"

    # -----------------------------
    # CABIN
    # -----------------------------

    if text == "business":

        result["cabin_class"] = "Business"
        result["confidence"] = "high"
        return result

    elif text == "first":

        result["cabin_class"] = "First"
        result["confidence"] = "high"
        return result

    elif text == "premium economy":

        result["cabin_class"] = "Premium Economy"
        result["confidence"] = "high"
        return result

    elif text == "economy":

        result["cabin_class"] = "Economy"
        result["confidence"] = "high"
        return result

    # -----------------------------
    # HOTEL
    # -----------------------------

    hotel_words = [
        "hotel",
        "stay",
        "accommodation",
        "room",
        "resort"
    ]

    if any(
        word in text
        for word in hotel_words
    ):

        result["needs_hotel"] = True

        nights_match = re.search(
            r"(\d+)\s+nights?",
            text
        )

        if nights_match:

            result["nights"] = int(
                nights_match.group(1)
            )

        near_match = re.search(
            r"near\s+([a-zA-Z\s]+)",
            text
        )

        if near_match:

            result[
                "hotel_location_preference"
            ] = (
                near_match.group(1)
                .strip()
                .title()
            )

    # -----------------------------
    # MODIFICATION
    # -----------------------------

    modification_words = [
        "change",
        "modify",
        "update",
        "instead",
        "replace",
        "switch"
    ]

    if any(
        word in text
        for word in modification_words
    ):

        result[
            "modification_request"
        ] = True

        destination_match = re.search(
            r"(destination\s+to|go\s+to)\s+([a-zA-Z\s]+)",
            text
        )

        if destination_match:

            result["destination"] = (
                destination_match.group(2)
                .strip()
                .title()
            )

    # -----------------------------
    # ROUND TRIP
    # -----------------------------

    round_trip = re.search(
        r"from\s+(.+?)\s+to\s+(.+?)\s+on\s+(.+?)\s+return\s+(.+)",
        text
    )

    if round_trip:

        result["origin"] = (
            round_trip.group(1).title().strip()
        )

        result["destination"] = (
            round_trip.group(2).title().strip()
        )

        result["departure_date"] = normalize_date(
            round_trip.group(3)
        )

        result["return_date"] = normalize_date(
            round_trip.group(4)
        )

        result["confidence"] = "high"

        return result


    # -----------------------------
    # SIMPLE ROUTE
    # -----------------------------

    route_match = re.search(
        r"from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+)$",
        text
    )

    if route_match:

        result["origin"] = (
            route_match.group(1)
            .strip()
            .title()
        )

        result["destination"] = (
            route_match.group(2)
            .strip()
            .title()
        )

        result["confidence"] = "high"

        return result


    # -----------------------------
    # ROUTE INSIDE SENTENCE
    # -----------------------------

    route_match = re.search(
        r"from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+)",
        text
    )

    if route_match:

        result["origin"] = (
            route_match.group(1)
            .strip()
            .title()
        )

        result["destination"] = (
            route_match.group(2)
            .strip()
            .title()
        )

        result["confidence"] = "high"

        return result

    # -----------------------------
    # DATE ONLY
    # -----------------------------

    if text in [
        "tomorrow",
        "next friday",
        "next monday"
    ]:

        result["departure_date"] = (
            normalize_date(text)
        )

        result["confidence"] = "high"

        return result
    # -----------------------------
    # YES / NO RESPONSES
    # -----------------------------

    if text == "yes":

        result["needs_hotel"] = True
        result["confidence"] = "high"

        return result

    if text == "no":

        result["needs_hotel"] = False
        result["confidence"] = "high"

        return result


    # -----------------------------
    # NIGHTS
    # -----------------------------

    night_match = re.search(
        r"(\d+)\s*nights?",
        text
    )

    if night_match:

        result["nights"] = int(
            night_match.group(1)
        )

        result["confidence"] = "high"

        return result


    # -----------------------------
    # PASSENGER NUMBER ONLY
    # -----------------------------

    if text.isdigit():

        result["passengers"] = int(text)

        result["confidence"] = "high"

        return result
    # -----------------------------
    # LLM EXTRACTION
    # -----------------------------

    prompt = f"""
Return ONLY JSON.

Schema:

{{
"origin":"",
"destination":"",
"departure_date":"",
"return_date":"",
"passengers":0,
"cabin_class":"",
"needs_hotel":false,
"nights":0,
"hotel_location_preference":"",
"modification_request":false,
"confidence":"high"
}}

User:

{user_input}
"""

    try:

        response = llm.invoke(prompt)

        content = (
            response.content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(content)

        if data.get("departure_date"):

            dep = str(
                data["departure_date"]
            )

            if re.match(
                r"\d{4}-\d{2}-\d{2}",
                dep
            ):

                year = int(
                    dep[:4]
                )

                current_year = (
                    datetime.now().year
                )

                if year < current_year:

                    dep = dep.replace(
                        str(year),
                        str(current_year),
                        1
                    )

                data["departure_date"] = dep

            else:

                data["departure_date"] = normalize_date(
                    dep
                )

        if data.get("return_date"):
            data["return_date"] = normalize_date(
                data["return_date"]
            )

        return data

    except Exception as e:

        print(
            f"Extractor Error: {e}"
        )

        return result