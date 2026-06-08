from langgraph.graph import StateGraph

from .nodes import (
    HotelState,
    validate_input,
    search_hotels,
    format_response
)

builder = StateGraph(HotelState)

builder.add_node(
    "validate_input",
    validate_input
)

builder.add_node(
    "search_hotels",
    search_hotels
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
    "search_hotels"
)

builder.add_edge(
    "search_hotels",
    "format_response"
)

graph = builder.compile()