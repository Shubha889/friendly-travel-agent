# Friendly Assistant Agent

A multi-agent travel booking system built with LangGraph and the A2A protocol.
The system includes an orchestrator agent, flight booking agent, hotel booking agent, and a Streamlit chat interface.

## Repository Structure

- `orchestrator/`
  - `agent.py` - Orchestrator LangGraph graph and dialogue logic
  - `prompts.py` - system prompt templates and orchestrator guidance
  - `state.py` - travel session state definition
  - `extractor.py` - travel detail extraction and normalization logic
- `agents/flight_agent/`
  - `agent.py` - Flight agent LangGraph graph
  - `mock_data.py` - mock flight inventory and search logic
  - `schemas.py` - A2A request/response schema models
- `agents/hotel_agent/`
  - `agent.py` - Hotel agent LangGraph graph
  - `mock_data.py` - mock hotel inventory and search logic
  - `schemas.py` - A2A request/response schema models
- `interface/`
  - `app.py` - Streamlit chat UI entry point
- `tests/`
  - unit test coverage for orchestrator and agents
- `docs/architecture.md` - architecture diagram and workflow overview
- `.env.example` - sample environment variables
- `.gitignore` - repository ignore rules for local files
- `requirements.txt` - Python dependencies

## Setup Instructions

1. Clone the repository:
   ```powershell
   git clone <your-repo-url>
   cd friendly-travel-agent
   ```

2. Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` if you need to customize environment variables:
   ```powershell
   copy .env.example .env
   ```

5. Run the Streamlit UI:
   ```powershell
   streamlit run interface/app.py
   ```

6. Open the browser when prompted and start chatting with the Friendly Travel Assistant.

## Running Tests

Run the test suite with:
```powershell
pytest
```

## What This Project Delivers

- Orchestrator agent handling user conversation and intent parsing
- Flight agent and hotel agent communicating via A2A request/response schemas
- LangGraph `StateGraph` workflows for orchestrator and sub-agents
- Multi-turn chat interface with clarifications and booking flow
- Mock flight and hotel search engines for realistic demo data
- Friendly conversational UX with aggregated results

## Architecture Notes

The orchestrator is the only user-facing agent. It maintains session state, understands intent, asks clarifying questions, and delegates flight/hotel tasks to sub-agents.

Sub-agents implement:
- input validation node
- search/retrieval node
- response formatting node

The A2A protocol is defined in `agents/*/schemas.py`:
- `A2ATaskRequest`
- `A2ATaskResponse`

See `docs/architecture.md` for the Mermaid diagram of the multi-agent workflow.

## Submission Checklist

1. Confirm repository contains:
   - `orchestrator/agent.py`
   - `agents/flight_agent/agent.py`
   - `agents/hotel_agent/agent.py`
   - `interface/app.py`
   - `tests/`
   - `requirements.txt`
   - `README.md`
   - `.env.example`
   - `docs/architecture.md`

2. Run `pytest` and ensure tests pass.
3. Run `streamlit run interface/app.py` and verify the UI starts.
4. Push the repository to GitHub.
5. Share the GitHub link for submission.

## Submission Instructions

- Use the repository link as your submission.
- Make sure the branch is up to date with your final changes.
- If a deadline is specified, submit before the deadline.
- Be prepared to demo the workflow, highlight how the A2A protocol is used, and explain the LangGraph graphs.

## Helpful Demo Prompts

- `I want to fly from Singapore to Tokyo on June 15 and need a hotel near Shinjuku for 5 nights.`
- `I only know I want to go to Tokyo. Can you ask me what else you need?`
- `Change the destination from Tokyo to Seoul and keep the same dates.`
- `Is June a good time to visit Tokyo?`
