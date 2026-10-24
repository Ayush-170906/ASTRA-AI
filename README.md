# ASTRA AI — Voice-Enabled Agentic AI Seminar Prototype

ASTRA AI is a Streamlit seminar prototype for exploring a safer, more inspectable agent workflow. It combines task planning, retrieval from a small local knowledge base, allowlisted tools, risk checks, human approval, outcome verification, and bounded retries. The interface includes an experimental browser-native voice assistant alongside text-based controls.

> **Current implementation:** The default/current environment uses a deterministic, rule-based provider. No live LLM is connected in the current environment. The prototype demonstrates simulated event-operations workflows; it does not verify or perform real-world actions. Notifications are mocked in memory and no real messages are sent.

## Problem statement

A system that can select tools and take actions needs controls beyond producing a fluent response. This prototype demonstrates how an agent can ground work in local information, check action risk, require human approval for high-risk tools, verify outcomes, and stop after a bounded number of retries.

## Features

- Streamlit interface with an Agent Workspace, four-scenario demo, Manual Mode, and expandable Technical Details.
- Experimental voice assistant using browser-native speech capabilities where available, with text input as fallback. Browser compatibility and live transcription behavior are not fully verified; voice should not be treated as a verified production feature.
- Custom-goal workflow with a visible execution trace and current status.
- Risk-based approval/denial controls for high-risk actions in Manual Mode.
- Allowlisted tools, local knowledge retrieval, verification, and bounded retry/escalation.
- A mock announcement tool that records only to an in-memory log; it does not send messages.
- Repeatable deterministic demo scenarios.

## Architecture and workflow

```text
User goal (typed or voice transcript)
    → Decompose → Plan → Retrieve local knowledge (TF-IDF)
    → Select allowlisted tool → Risk gate
    → Human approval when required → Execute → Verify
    → Bounded retry or final result
```

The Streamlit UI is in `04_PROTOTYPE/app.py`. `agent/` holds the workflow controller, state, decomposition, planning, and demo orchestration. `rag/` loads and retrieves local knowledge using **scikit-learn TF-IDF vectors and NumPy cosine similarity**; FAISS is not implemented. `tools/` contains the registry and tool implementations. `safety/` contains risk classification and approval logic, and `verification/` checks action outcomes. `llm/` contains provider interfaces/adapters and the deterministic rule-based fallback. Demo Mode uses the deterministic provider to keep scenario outcomes repeatable.

## Technology stack

- Python and Streamlit
- scikit-learn TF-IDF and NumPy cosine similarity for retrieval
- pytest for automated tests
- Browser-native speech recognition and speech synthesis APIs for the experimental voice interface, where the browser supports them
- Optional Ollama and Anthropic provider adapters exist in the code, but no live LLM is connected in the current environment

## Repository structure

```text
01_OFFICIAL/       Seminar source material
02_WORKING/        Working documents
03_RESEARCH/       Research material
04_PROTOTYPE/      Streamlit app, agent modules, knowledge, assets, and tests
05_FINAL/          Final seminar material
06_REPORTS/        Project reports
```

For implementation details, see [Prototype Documentation](04_PROTOTYPE/README.md).

## Prerequisites

- Windows 10/11
- Python 3.11 recommended
- PowerShell
- Internet access to install the Python dependencies

The deterministic demo does not require an API key or an external model service. Optional provider configuration is described in `04_PROTOTYPE/.env.example`; credentials should remain local and must not be committed.

## Setup and run (Windows PowerShell)

Run these commands from the repository root. Calling the virtual environment's Python directly avoids the need to enable PowerShell script activation:

```powershell
cd .\04_PROTOTYPE
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Demo scenarios

Click **Run Demo** to run the four fixed scenarios:

1. Normal multi-step event-preparation workflow.
2. High-risk action with simulated approval.
3. High-risk action with simulated denial; the denied action is not executed.
4. Forced verification failures followed by bounded retries and escalation.

The demo's approval/denial choices are simulated for a repeatable walkthrough. In **Manual Mode**, a custom goal can pause for a human to approve or deny a high-risk action through the UI.

## Safety controls

- Tools are selected from an allowlisted registry and have declared risk levels.
- High-risk actions pause for approval in Manual Mode; denial prevents that action from executing.
- Demo Mode explicitly labels its approval decisions as simulated.
- Verification failures are retried only within a configured bound, after which the run escalates.
- The announcement tool is a mock: its in-memory log is for demonstration, and no real messages are sent.

## Tests

From the repository root, run:

```powershell
cd .\04_PROTOTYPE
.\.venv\Scripts\python.exe -m pytest tests -v
```

The suite covers tool behavior, the risk/approval gate, retrieval, bounded retries, agent workflows, and demo scenarios.

## Limitations

- The current environment uses deterministic, rule-based behavior; no live LLM is connected. Optional provider adapters require separate configuration and availability.
- Voice features depend on browser-native APIs and browser permission. Live transcription and wake-word behavior have not been fully verified across browsers; use text input as the dependable fallback.
- Retrieval uses a small local TF-IDF index, not FAISS or a neural embedding service.
- Notifications and other external actions are not connected to real services. No real messages are sent.
- This is an educational seminar prototype, not a production-ready or deployed agent.

## Future scope

- Configure and evaluate a live model provider while preserving deterministic demos and the safety gate.
- Verify voice behavior in supported browsers and document tested permissions, recognition, and fallback behavior.
- Expand test/evaluation coverage and assess persistence and operational requirements before considering external integrations or deployment.
