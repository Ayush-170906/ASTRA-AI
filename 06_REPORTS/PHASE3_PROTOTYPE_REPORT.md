# Phase 3 — Prototype Completion Report

Location: [04_PROTOTYPE/](../04_PROTOTYPE/) — see [README.md](../04_PROTOTYPE/README.md) for setup,
architecture detail, and the live demo script.

Built against the PRD/TRD the student locked at Phase 3 kickoff. This report maps what was built to
that spec, calls out every deviation explicitly, and verifies each acceptance criterion.

---

## Locked decisions — what was actually built

| Decision | Locked value | Built as |
|---|---|---|
| Language | Python | Python 3.11 |
| UI | Streamlit | Streamlit, single-page dashboard |
| Agent controller | Custom lightweight controller | Custom resumable FSM (`agent/controller.py`) — no LangChain/LangGraph/CrewAI |
| LLM | Provider-agnostic adapter | `llm.base.LLMProvider` ABC, one method: `generate(prompt) -> str` |
| Primary LLM mode | Local-first | Implemented — see deviation note below |
| Local runtime | Ollama-compatible | `llm/local.py`, plain HTTP, no `ollama` package dependency |
| API | Optional fallback | `llm/api.py`, Anthropic Messages API, key from env only |
| RAG | Local | `rag/` — chunk, embed, retrieve, all in-process |
| Vector store | FAISS | **Deviation: TF-IDF + numpy cosine similarity** (see below) |
| Memory | In-memory state | `agent.state.AgentState` dataclass, no database |
| Tools | 3-4 controlled tools | 4: `calculate_capacity`, `generate_checklist`, `search_knowledge`, `mock_send_announcement` |
| High-risk action | Mock notification | `mock_send_announcement` — appends to an in-memory list only |
| Human approval | Mandatory for HIGH | Enforced in `safety/approval.py`, the single gate every tool call passes through |
| Retry | MAX_RETRIES = 2 | Implemented exactly, in `AgentState.max_retries` |
| Database | None | None |
| Authentication | None | None |
| Real external actions | None | None — verified by test and by design (no network/SMTP/DB client code anywhere) |
| Multi-agent | Future scope | Not implemented |
| Deployment | Local laptop | `streamlit run app.py`, no deployment config |
| Tests | Unit + integration + demo scenarios | 19 tests, 5 files, all passing |

## Two documented deviations

**1. Vector store: TF-IDF + numpy cosine similarity, not FAISS.**
The knowledge base is four short text files (a few dozen chunks after chunking). FAISS's approximate-
nearest-neighbor indexing solves a million-vector search problem this prototype does not have, and it
is a common source of native-build install failures on Windows. TF-IDF + brute-force cosine similarity
retrieves the same top-k result at this scale with a pure Python/numpy dependency chain and no model
download. `rag/retriever.py` is the seam where FAISS + a real embedding model could be substituted later
without touching any calling code.

**2. LLM provider: a third deterministic fallback was added, beyond "local-first + API fallback."**
This deployment environment has neither a reachable Ollama server nor an `ANTHROPIC_API_KEY` (both
checked programmatically before writing any code — no Ollama process, no key in environment). Rather
than leave the prototype undemonstrable without further setup the student would need to do, a
deterministic `RuleBasedProvider` (`llm/rule_based.py`) was added as the guaranteed-available third
tier. It satisfies the exact same `LLMProvider.generate(prompt) -> str` interface the TRD specifies, so
every other module is unaffected — `agent/decomposer.py` builds the same JSON-structured prompt and
parses the same JSON response regardless of which of the three providers answers it. Swapping in a real
Ollama server or an API key activates the corresponding provider automatically, with zero code changes;
see README.md's "LLM provider" section for exact steps.

This was a judgment call made to keep the prototype buildable and demonstrable end-to-end in this
session; it is surfaced here for the student's approval rather than presented as silently equivalent to
the original plan.

---

## Architecture as built

```
Streamlit UI (app.py)
        │
        ▼
Agent Controller (agent/controller.py) ── resumable FSM, one micro-stage per call
        │
        ├── analyze_goal + decompose  (agent/decomposer.py)  ← LLMProvider
        ├── Planner                    (agent/planner.py)
        ├── Retriever                  (rag/retriever.py)     ← TF-IDF vector store
        ├── ToolRegistry                (tools/registry.py)    ← allowlist, 4 tools
        ├── Safety gate                 (safety/approval.py + safety/risk.py)
        └── Verifier                    (verification/verifier.py)
```

Every AgentStatus transition (`IDLE → PLANNING → RETRIEVING → SELECTING_TOOL → RISK_CHECK →
[WAITING_FOR_APPROVAL] → EXECUTING → OBSERVING → VERIFYING → [REPLANNING] → COMPLETED / ESCALATED /
TERMINATED`) is logged as a numbered `TraceEvent`, which is what the dashboard's execution trace
displays — the same schema described in the PRD's section 17.

**Why a step machine instead of the TRD's blocking `while` pseudocode:** Streamlit reruns the entire
script on every user interaction, so a blocking call waiting on a button click is not possible. The
controller instead advances one stage at a time and returns to the caller at `WAITING_FOR_APPROVAL` or
any terminal status; the Streamlit app calls it again after the user clicks Approve/Deny, and the same
function drives the test suite by pre-setting `approval_status` before calling it once.

**The one rule the whole safety layer exists to enforce:** `safety/approval.py::gate()` is the only
function that decides whether a task's tool may run, and its authoritative risk input is the *tool's own
registered* `risk_level` from the allowlisted registry — never whatever risk label an LLM proposed during
decomposition. An LLM can propose a `risk` field in its JSON output, but `agent/controller.py`'s
RISK_CHECK stage always overrides it with the registry's value before the gate ever runs. This closes the
obvious hole where a model could talk its way past the gate by under-reporting its own action's risk.

---

## Bugs found and fixed during this build (via testing, not left for the student to find)

1. **Decomposition keyword overlap.** `RuleBasedProvider`'s keyword heuristic originally included
   "event" as a trigger for the brief/capacity/checklist scenario. Since the high-risk demo goal ("Send
   the event announcement...") also contains "event," it was incorrectly generating all four tasks
   instead of just the announcement — meaning three LOW-risk tools would execute before the HIGH-risk
   one was even reached. Caught by `tests/test_agent.py::test_B_high_risk_action_pauses_then_executes_on_approval`.
   Fixed by removing "event" from the brief-scenario keyword list (documented in the code comment).
2. **Resume-after-approval bug.** `run_until_pause`'s loop condition was `while status not in
   PAUSE_STATUSES`, but `WAITING_FOR_APPROVAL` is itself one of the pause statuses — so calling it a
   second time after the human clicked Approve/Deny saw "already paused" and did nothing, meaning a
   **denied action would never actually terminate** (it stayed stuck at `WAITING_FOR_APPROVAL` forever).
   Caught by `tests/test_agent.py::test_B_high_risk_action_never_executes_when_denied`. Fixed by
   re-entering the `RISK_CHECK` stage at the top of `run_until_pause` whenever the state is paused for
   approval and a decision has since been recorded.

Both fixes were verified twice: once via the automated test suite, and a second time by manually driving
the running Streamlit app in a browser through all three high-risk paths (approve, deny) and the
retry/escalation path, confirming the UI behaves identically to the tests.

---

## Acceptance criteria (PRD section 27)

**Architecture** — all present and exercised by tests or the live browser run: goal analyzer, task
decomposition, planner, RAG, tool registry, tool selection, risk gate, human approval, execution,
observation, verification, retry, escalation, final response. ✅

**Safety:**
- High-risk action cannot bypass approval — ✅ enforced structurally (single `gate()` call site), verified
  by `tests/test_risk_gate.py` and `tests/test_agent.py::test_safety_violation_rate_is_zero_across_all_scenarios`.
- Denied action never executes — ✅ verified by test and live browser run.
- Retry is bounded — ✅ `tests/test_retry.py::test_retries_exhausted_escalates` proves exactly
  `MAX_RETRIES + 1` attempts occur, never more.
- No arbitrary code execution — ✅ the tool registry is a static allowlist; an LLM can only *name* an
  already-registered tool, never supply code to run.
- No real external destructive operations — ✅ `mock_send_announcement` only appends to an in-memory
  Python list; no network/SMTP/DB client exists anywhere in the codebase.
- Secrets are protected — ✅ `ANTHROPIC_API_KEY` read only from environment, `.env` gitignored,
  `.env.example` has no real value.

**Demonstration** — all five scenarios run successfully, verified live in a browser (not just unit
tests): normal successful run, high-risk approval run, high-risk denial run, bounded-retry-then-escalate
run, RAG grounding visible in the trace on every run. ✅

## Test results

28/28 tests passing (`pytest tests/ -v`): the original 19 (4 tool, 6 risk-gate, 2 RAG, 2 retry/escalation,
5 integration) plus 9 new Demo Mode tests (`tests/test_demo.py`), added in the round below. None of the
original 19 were modified or weakened.

## Remaining items for the student

1. **Review the two documented deviations** (vector store, LLM fallback tier) and confirm they're
   acceptable for submission, or specify a preference (e.g., install Ollama before the seminar for a real
   LLM-driven decomposition instead of the rule-based one).
2. **Rehearse the live demo script** in README.md at least once end-to-end before presenting.
3. Optional: if a real LLM backend is wanted for the seminar, install Ollama and pull a model, or set
   `ANTHROPIC_API_KEY` — no code changes are needed either way.

---

## Addendum — Demo Mode UI enhancement (Round 2)

A focused addition requested after the core prototype was already built and browser-verified: a single
**"▶ RUN FULL DEMO"** button that runs all four validated PRD scenarios automatically, with no manual
input, for a reliable one-click seminar walkthrough. No architecture change — this only calls the
existing `agent.controller.start`/`run_until_pause` four times with fixed goals and, where a real user
would click Approve/Deny, a logged simulated decision instead.

### Why it was added
The student asked for a way to start the complete demonstration with one click during the actual seminar,
without manually re-entering goals or toggling the retry-demo checkbox for each scenario, and without the
demo ever stalling on a real approval click while presenting live.

### How it works
- **New module, `agent/demo.py`** — pure functions, no Streamlit dependency, so it's directly unit-testable.
  `run_full_demo(deps)` runs four scenarios, each against a **fresh `AgentState`**, and returns a list of
  `ScenarioResult(number, total, name, state, expected_status)` with a `.passed` property
  (`state.status == expected_status`) and a `.label` property (`"Scenario N/4: <name>"`).
- **Scenario 1 (Normal Execution)** — the same brief/capacity/checklist goal used in Manual Mode's default,
  run to completion with no approval needed (all LOW risk). Expected terminal status: `COMPLETED`.
- **Scenario 2 (High-Risk Approval)** — the announcement goal; when the loop pauses at
  `WAITING_FOR_APPROVAL`, `agent/demo.py` logs `"DEMO MODE — Simulated Human Approval: APPROVED"` as its
  own trace event, sets `state.approval_status = "APPROVED"` (the exact same field the real APPROVE button
  sets), and resumes. Expected: `COMPLETED`.
- **Scenario 3 (High-Risk Denial)** — identical setup, simulated `"DENIED"` instead. Expected: `TERMINATED`.
- **Scenario 4 (Bounded Retry → Escalation)** — the brief goal again, with the existing
  `demo_force_fail_task_desc_contains`/`demo_force_fail_remaining` fields (already part of `AgentState`
  from the original build, previously only reachable via the sidebar checkbox) set to force exactly
  `MAX_RETRIES + 1 = 3` failures on the capacity subtask. Expected: `ESCALATED`, with exactly 2
  `REPLANNING` events and 3 `VERIFY … FAIL` events — verified by test and by reading the live trace in the
  browser.
- **UI (`app.py`)** — a "🎓 SEMINAR DEMO MODE" section was added above the existing goal input, with the
  RUN FULL DEMO / RESET DEMO buttons, a Demo Summary (🟢/🔴 per scenario, `N / 4 scenarios passed`), and
  one collapsible panel per scenario labeled `🔵 DEMO — Scenario N/4: <name>`, each rendering that
  scenario's full trace through the **same `render_trace()` function** Manual Mode uses (extracted from
  the previously inline trace-rendering code so the two can never drift apart). Manual Mode's goal input,
  RUN AGENT button, real APPROVE/DENY buttons, sidebar demo controls, and its own execution trace are all
  unchanged and fully functional — verified live in the browser after the Demo Mode changes landed.

### Documented deviation: Demo Mode always uses the deterministic provider
The PRD requires Demo Mode to "reliably demonstrate the architecture every time" and to "not depend on
unpredictable LLM output." A real Ollama or API provider could legitimately vary its decomposition output
between runs. So `agent/demo.py::demo_dependencies()` constructs a `Dependencies` object that reuses
Manual Mode's already-built `retriever` and `registry` (same knowledge base, same tools — nothing about
the world changes) but always substitutes a fresh `RuleBasedProvider` for the LLM, regardless of what
Manual Mode is configured with. This means Demo Mode's four traces are byte-for-byte reproducible on every
click. Manual Mode is completely unaffected — it still receives whatever `get_llm_provider()` selected.

### Two bugs this round's own tests would have caught, had they existed in the original build
None — this round found no new defects in the existing controller/safety/verification code; the 19
original tests and the two bugs fixed in Round 1 (documented above) already covered the paths Demo Mode
now also exercises automatically. `tests/test_demo.py`'s 9 tests exist to pin down Demo Mode's *own* new
behavior (exact scenario count, exact retry count, no hanging, no extra mock sends, simulated-decision
logging) rather than to catch further core-loop bugs.

### Verification performed
- `pytest tests/ -v` → 28/28 passing (19 original, unmodified, + 9 new).
- Live browser run: clicked RUN FULL DEMO → Demo Summary showed `4 / 4 scenarios passed`; expanded all
  four scenario panels and confirmed the traces match the PRD's specified sequences exactly, including
  the `✅ DEMO MODE — Simulated Human Approval: APPROVED` and `🚫 DEMO MODE — Simulated Human Approval:
  DENIED` lines, and exactly two `REPLANNING` events + one `ESCALATE` event in Scenario 4.
- Live browser run: clicked RESET DEMO → summary and all four panels cleared, button correctly disabled
  again.
- Live browser run: used Manual Mode (default goal, RUN AGENT) after running Demo Mode → completed
  normally, fully independent of the Demo Mode results shown above it.
- Confirmed no real external action occurs: `get_sent_log()` grows by exactly one entry per full demo run
  (from the one approved scenario), never from the denied one — asserted in
  `test_demo_causes_no_real_external_action_beyond_the_mock_log`.

### Final output summary
- **Files changed:** `04_PROTOTYPE/app.py` (Demo Mode UI section added, trace rendering extracted into
  `render_trace()`, Manual Mode section relabeled and otherwise untouched); **files added:**
  `04_PROTOTYPE/agent/demo.py`, `04_PROTOTYPE/tests/test_demo.py`; **docs updated:**
  `04_PROTOTYPE/README.md`, this report.
- **Demo Mode entry point:** the `▶ RUN FULL DEMO` button at the top of the Streamlit app.
- **Exact button label:** `▶ RUN FULL DEMO` (and `↻ RESET DEMO` alongside it).
- **All 19 existing tests still pass:** yes, unmodified.
- **New tests added:** 9 (`tests/test_demo.py`), all passing.
- **All four scenarios pass in the browser:** yes, confirmed live (4/4).
- **Manual Mode still works:** yes, confirmed live, fully independent of Demo Mode state.
- **Demo Mode completes without any user interaction:** yes — approval/denial are simulated and logged as
  such; the loop never pauses at `WAITING_FOR_APPROVAL` in Demo Mode.
- **Issues found:** none in this round; the two bugs fixed were both in Round 1 and are documented above,
  not newly introduced or newly discovered here.
