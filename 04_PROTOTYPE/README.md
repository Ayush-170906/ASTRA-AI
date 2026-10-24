# Agentic AI Reliability Loop — Phase 3 Seminar Prototype

A small, safe, demonstrable implementation of the seminar's proposed control loop:

```
Goal → Decompose → Plan → Retrieve → Tool Selection → Risk Gate →
Human Approval → Execute → Observe → Verify → Bounded Retry → Result
```

This is the prototype referenced by the approved PPT and synopsis
(`Agentic AI: Autonomous Goal-Oriented Intelligent Systems for Planning,
Reasoning and Task Execution`). It follows the PRD/TRD locked in Phase 3
kickoff, with the deviations below called out explicitly rather than
silently substituted.

## Quick start

```bash
cd 04_PROTOTYPE
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501). No `.env`
file or API key is required to run the demo — see "LLM provider" below.

Run the test suite:

```bash
pytest tests/ -v
```

## What this proves, and why it isn't "just a chatbot"

A conventional chatbot is `User → Prompt → LLM → Response`. This prototype
instead runs every goal through the full loop above: it decomposes the
goal into subtasks, grounds each one in a local knowledge base (RAG),
selects a tool from an allowlisted registry, classifies that tool's risk,
**stops and waits for explicit human approval before any high-risk action
executes**, executes, observes the result, verifies it against an expected
outcome, and retries a bounded number of times before escalating.

The most important design decision, and the answer to "what's your
contribution beyond using an LLM?":

> The prototype focuses on the control layer around the LLM: structured
> planning, tool selection, pre-action risk gating, human approval for
> high-risk actions, post-action verification, and bounded recovery. The
> LLM (or the deterministic fallback standing in for it in this
> environment) is treated as a reasoning component that *proposes*
> structured actions — it never executes anything directly. The tool
> registry, risk gate, and verifier are what actually decide what happens.

## LLM provider: what's actually running, and why

*(This section describes Manual Mode's provider selection. Demo Mode has
its own fixed policy — always deterministic — explained in "Running the
Seminar Demo" below.)*

The TRD's locked decision is "local-first (Ollama) + API fallback." This
deployment environment has **neither** a running Ollama server **nor** an
`ANTHROPIC_API_KEY` configured (both were checked at build time). Per the
TRD's own provider-agnostic principle, the controller doesn't know or care
which backend produced its text — so a third, deterministic provider
(`llm/rule_based.py`) was added to guarantee the prototype runs and
demonstrates the full loop with zero setup, cost, or internet dependency.

Provider selection order (`llm/__init__.py::get_llm_provider`):
1. **Local Ollama** (`llm/local.py`) — used automatically if a server is
   reachable at `OLLAMA_HOST` (default `http://localhost:11434`). Install
   Ollama, pull a model (`ollama pull llama3.1`), and it activates with no
   code changes.
2. **Anthropic API** (`llm/api.py`) — used if `ANTHROPIC_API_KEY` is set
   (copy `.env.example` to `.env` and fill it in, or export it in your
   shell). Never hardcoded, never logged.
3. **Rule-based fallback** (`llm/rule_based.py`) — always available,
   deterministic, and what actually drives this demo in this environment.
   It recognizes the two documented demo goals by keyword and produces the
   same structured JSON output a real LLM would be asked for, so every
   other module (decomposer, planner, verifier, controller) runs
   identically regardless of which provider is active.

The active provider is shown at the top of the dashboard on every run.

## Deviation from the TRD: vector store

The TRD names FAISS + neural embeddings. This prototype uses scikit-learn
TF-IDF vectors with brute-force numpy cosine similarity instead
(`rag/vectorstore.py`). Reasoning: the knowledge base is four short text
files (a few dozen chunks) — FAISS's approximate-nearest-neighbor indexing
solves a million-vector search problem this prototype doesn't have, and it
adds a native-build dependency that's a common source of install failures
on Windows, plus a neural embedding model would need to be downloaded. The
`Retriever` class is the seam where FAISS + a real embedding model could
be swapped in later without touching any calling code, if the knowledge
base grows enough to need it.

## Project structure

```
04_PROTOTYPE/
├── app.py                     Streamlit dashboard
├── requirements.txt
├── .env.example
├── agent/
│   ├── state.py               AgentState, AgentStatus, SubTask, TraceEvent
│   ├── controller.py          The FSM implementing the full reliability loop
│   ├── decomposer.py          Goal analysis + LLM-driven task decomposition
│   ├── planner.py             Task ordering / replan-on-failure
│   └── demo.py                Demo Mode orchestration (4 fixed scenarios, simulated approvals)
├── llm/
│   ├── base.py                LLMProvider interface
│   ├── local.py                Ollama adapter
│   ├── api.py                  Anthropic API adapter
│   └── rule_based.py           Deterministic fallback (active by default here)
├── rag/
│   ├── loader.py               Chunking
│   ├── vectorstore.py          TF-IDF + cosine similarity
│   └── retriever.py            Retriever facade used by the search_knowledge tool
├── tools/
│   ├── registry.py             Tool/ToolResult/ToolRegistry (the allowlist)
│   ├── calculator.py           calculate_capacity (LOW risk)
│   ├── knowledge_lookup.py     search_knowledge, generate_checklist (LOW risk)
│   └── mock_notification.py    mock_send_announcement (HIGH risk, never real)
├── safety/
│   ├── risk.py                  requires_approval()
│   └── approval.py              The one approval gate every tool call passes through
├── verification/
│   └── verifier.py              Expected-vs-observed PASS/FAIL with a reason
├── knowledge/                   The local knowledge base (4 .txt files)
└── tests/                       19 unit + integration tests (see below)
```

## Tools and their risk levels

| Tool | Risk | What it does |
|---|---|---|
| `search_knowledge` | LOW | Retrieve relevant chunks from the local knowledge base |
| `calculate_capacity` | LOW | Deterministic arithmetic: capacity − registered |
| `generate_checklist` | LOW | Return the standard event-preparation checklist |
| `mock_send_announcement` | **HIGH** | Appends to an in-memory log only — **never sends anything real** |

Risk is a static property declared on the tool in the registry, not
something the LLM self-reports — the controller always looks up the
tool's own registered `risk_level` at the risk-check stage, so a model
cannot talk its way past the gate by under-reporting risk on its own
proposed action (see the docstring in `agent/controller.py`).

## Running the Seminar Demo

The dashboard has two modes, both always available:

- **🎓 Seminar Demo Mode** (top of the page) — one button, runs all four
  PRD-validated scenarios back to back, deterministically, with no manual
  input. This is what you use live in front of an evaluator.
- **🧑‍💻 Manual Mode** (below it, unchanged from before) — type your own
  goal, click RUN AGENT, and click real APPROVE/DENY buttons yourself.
  Demo Mode never disables or replaces this.

### Steps

1. `streamlit run app.py`
2. Open the URL Streamlit prints in your browser.
3. Click **▶ RUN FULL DEMO**.
4. Observe: a spinner runs briefly, then a **Demo Summary** appears
   (🟢/🔴 per scenario, `4 / 4 scenarios passed`), followed by four
   expandable panels — `🔵 DEMO — Scenario 1/4` through `4/4` — each
   containing that scenario's full execution trace, exactly like Manual
   Mode's trace (same renderer, same stage-by-stage detail; nothing about
   the underlying agent is hidden or summarized away).
5. Click **↻ RESET DEMO** to clear the results and run again, or just
   click RUN FULL DEMO again — it always resets its own state first.

### What each scenario proves, and what to say while it runs

**Scenario 1/4 — Normal Execution.** Expand it and point at the trace:
GOAL → DECOMPOSE (3 subtasks) → per subtask, PLAN → RETRIEVE (the RAG
grounding step — point out the retrieved knowledge chunks) → TOOL_SELECT →
RISK_CHECK (all LOW) → EXECUTE → OBSERVE → VERIFY (PASS) → `COMPLETED`.
*"This is the agent handling an ordinary multi-step goal — not a chatbot
reply, a sequence of grounded, verified actions."*

**Scenario 2/4 — High-Risk Approval.** The trace shows RISK_CHECK = HIGH,
then a line reading `✅ DEMO MODE — Simulated Human Approval: APPROVED`,
then EXECUTE. *"In a live session a human clicks Approve here — for the
demo we simulate that decision so the walkthrough doesn't stall, but it's
the exact same approval field the real button sets."* Mention the mock
announcement log at the bottom of the page proves nothing was ever really
sent.

**Scenario 3/4 — High-Risk Denial.** Same setup, but the trace shows
`🚫 DEMO MODE — Simulated Human Approval: DENIED` and the run ends at
`TERMINATED` with **no EXECUTE event at all** for that tool. *"This is
Principle 1 — a denied high-risk action never runs, full stop."*

**Scenario 4/4 — Bounded Retry → Escalation.** Point out exactly two
`REPLANNING` events and three `VERIFY … FAIL` events (the original attempt
plus 2 retries) before `ESCALATE` and `ESCALATED`. *"MAX_RETRIES=2 is
enforced structurally — three total attempts, never more, then it stops
and asks for a human instead of looping forever."*

Target duration for all four, expanding each trace briefly: **3–5
minutes** — matches the seminar's presentation slot.

### Why Demo Mode is deterministic

Manual Mode uses whichever LLM provider `llm.get_llm_provider()` selected
for this environment (Ollama, the Anthropic API, or the rule-based
fallback — shown at the top of the page). **Demo Mode always uses the
deterministic rule-based provider internally, regardless of what Manual
Mode is using**, specifically so the four scenarios produce the same
trace, the same PASS/FAIL outcome, and the same retry counts on every
click — a real LLM could legitimately phrase or order subtasks
differently between runs, which would undermine "reliably demonstrate the
architecture every time." See `agent/demo.py`'s module docstring and
`PHASE3_PROTOTYPE_REPORT.md` for the full reasoning. This is a documented
addition on top of the original PRD/TRD, not a silent substitution, and it
does not touch or weaken Manual Mode in any way.

## Tests

28 tests across 6 files, all passing:

```
tests/test_tools.py        Each tool's happy path and failure path
tests/test_risk_gate.py    The approval gate's every decision branch,
                            including the invariant that DENIED can never
                            be reinterpreted as PROCEED
tests/test_rag.py          Retrieval finds relevant chunks, and returns
                            (almost) nothing for an unrelated query
tests/test_retry.py        Bounded retry succeeds after N<MAX_RETRIES
                            failures; exhausting retries escalates and
                            never loops indefinitely
tests/test_agent.py        The PRD's four integration scenarios (A-D) plus
                            a cross-cutting Safety Violation Rate check
                            (target 0, per the seminar's evaluation
                            framework): no HIGH-risk tool may ever appear
                            in an EXECUTE event without a preceding
                            APPROVED event in the same run
tests/test_demo.py         Demo Mode (agent/demo.py), independent of
                            Streamlit: all 4 scenarios pass, none ever
                            leaves a scenario WAITING_FOR_APPROVAL (i.e.
                            Demo Mode never hangs), simulated approval/
                            denial are logged and enforced exactly like
                            the real gate, scenario 4 does exactly 2
                            retries / 3 total attempts, and running the
                            whole demo twice never sends more than one
                            real mock notification per approved scenario
```

## Explicit non-goals (unchanged from the PRD)

No real email/message sending, no real payments, no database mutation, no
credential access, no shell/arbitrary code execution from LLM output, no
filesystem-destructive actions, no multi-agent collaboration in this
version, no production deployment claim. Everything here is a local,
single-process, in-memory demo.

## Known limitations

- The rule-based provider only recognizes the two documented demo goals by
  keyword; an arbitrary goal gets a single generic `search_knowledge` task
  rather than a tailored decomposition. Swapping in a real LLM (Ollama or
  the API adapter) removes this limitation, since `agent/decomposer.py`'s
  prompt and JSON-parsing logic work identically regardless of provider.
- State is in-memory and per-process (`AgentState`, plus the mock
  notification log) — restarting the Streamlit server clears everything,
  by design (no database, per the locked PRD/TRD decisions).
- The verifier's numeric-comparison heuristic works well for the
  calculator tool but is a light heuristic, not a general-purpose semantic
  verifier; this is an appropriate scope for a seminar-level prototype.
