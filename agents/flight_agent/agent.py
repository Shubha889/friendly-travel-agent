from langgraph.graph import StateGraph

from .nodes import (
    FlightState,
    validate_input,
    search_flights,
    format_response
)

builder = StateGraph(FlightState)

builder.add_node(
    "validate_input",
    validate_input
)

builder.add_node(
    "search_flights",
    search_flights
)

builder.add_node(
    "format_response",
    format_response
)

builder.set_entry_point(
    "validate_input"
)

builder.add_edge(
    "validate_input",
    "search_flights"
)

builder.add_edge(
    "search_flights",
    "format_response"
)

graph = builder.compile()