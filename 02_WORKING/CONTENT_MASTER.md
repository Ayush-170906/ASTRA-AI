# CONTENT MASTER — Agentic AI Technical Seminar
Topic: "Agentic AI: Autonomous Goal-Oriented Intelligent Systems for Planning, Reasoning and Task Execution"
Student: Korde Ayush Sandeep | PRN 72406771M | Roll 32 | T.E. IT, Sem I, AY 2026-27
Guide: Prof. V. A. Khairnar | Coordinator: Prof. S. D. Pingale | HOD: Dr. S. R. Lahane

This is the single source of truth for text content. PPT (22 slides, revised in Phase 2) and Synopsis
(revised in Phase 2) both draw from this document, repartitioned to fit their own template structure
(Section E of the audit). Citations use [n] keyed to 03_RESEARCH/LITERATURE.md.

**Phase 2 revision note:** the PPT's Algorithm slide now presents the loop below as a visual box/arrow
flow diagram (native shapes, not dense pseudocode) for projector readability. The pseudocode is retained
here as the precise technical specification the diagram must match.

---

## 1. ABSTRACT (200-300 words, for synopsis)

Agentic AI refers to AI systems that go beyond single-turn generation to autonomously pursue a
user-specified goal by planning, invoking tools, observing outcomes, and adapting their next action —
without step-by-step human instruction for every action [1]. Unlike conventional rule-based automation,
generative AI, and standalone large language models (LLMs), which respond to a single prompt or a fixed
pipeline, an agentic system decomposes a goal into subtasks, retrieves relevant knowledge, selects and
invokes tools or APIs, and verifies its own results before proceeding [1][2][3]. Prior work has
separately advanced planning and reasoning-action interleaving (ReAct) [4], memory and
retrieval-augmented generation (RAG) [7], and multi-agent workflow coordination [5]; a parallel body of
work catalogs the security, privacy, and ethical risks that arise once such agents are permitted to act
autonomously [6]. However, these two threads are rarely integrated into a single, demonstrable control
loop: most reported architectures optimize for task capability, while risk assessment and outcome
verification are treated as afterthoughts rather than first-class stages of the loop.
This seminar surveys the core building blocks of Agentic AI — goal understanding, task decomposition,
planning, memory/RAG, tool use, observation, and verification — and proposes a reliability-oriented
agent architecture that explicitly separates planning from execution and pre-action risk screening from
post-action verification, with bounded human-in-the-loop approval for high-risk actions and a
retry/escalation policy bounded by a maximum retry count. The seminar evaluates this proposal
qualitatively against a structural checklist of correctness (Section on Evaluation Framework) rather than
against fabricated experimental results, and outlines a small prototype that demonstrates the loop end to
end on safe, non-destructive tools. The intended contribution is a clear, teachable reference architecture
that makes reliability an explicit design concern in Agentic AI rather than an implicit assumption.

**Word count target: 220-260 words.**

---

## 2. KEYWORDS (comma-separated, no bullets, TNR 12 bold italic per template)

Agentic AI, autonomous agents, large language models, task planning, task decomposition,
retrieval-augmented generation, tool use, reasoning and acting, human-in-the-loop, verification,
risk assessment, multi-agent systems

---

## 3. INTRODUCTION

Artificial intelligence systems have evolved through three broad stages relevant to this seminar:
(a) rule-based / conventional AI, which executes fixed logic with no learning or adaptation;
(b) generative AI and large language models (LLMs), which produce fluent text, code, or other content in
response to a prompt but do not, by themselves, act in the world or pursue a goal across multiple steps;
and (c) **Agentic AI**, which uses an LLM (or a similar reasoning engine) as a controller inside a loop
that plans, retrieves knowledge, selects tools, executes actions, observes outcomes, and decides whether
to continue, retry, or stop [1][2][3]. The distinguishing property of an agentic system is *autonomous,
goal-directed, multi-step behavior*: given a goal such as "compile this data and file the report," the
system determines the sequence of sub-actions itself, rather than being told each step individually.
This distinction matters practically: a conventional chatbot can explain how to do something, while an
agentic system can attempt to actually do it — which is precisely why reliability, safety, and
verification are central design concerns, not optional extras, once a system is permitted to act.

### 3.1 Motivation
- LLMs are increasingly connected to real tools, APIs, files, and services, so a single incorrect or
  unverified action (e.g., sending a wrong email, executing a bad database query, or making an
  unintended purchase) has real consequences — motivating an architecture where risk is assessed
  *before* an action executes, not only inspected after the fact [6].
- Existing literature richly covers individual capabilities — planning, ReAct-style reasoning [4],
  memory/RAG [7], and multi-agent coordination [5] — but rarely packages them into one teachable,
  reliability-first reference loop that a student or engineer can actually build and demonstrate.
- T.E. IT students entering industry will encounter agent frameworks (LangChain/LangGraph-style tool-
  calling agents, coding agents, workflow copilots) as part of everyday tooling; understanding the
  underlying control loop — not just prompting an LLM — is a foundational, transferable skill.

### 3.2 Objectives
1. Define Agentic AI precisely and distinguish it from conventional AI, generative AI, and standalone LLMs.
2. Survey the core components of an agentic loop — planning, task decomposition, memory/RAG, tool use,
   observation, and verification — grounded in verifiable literature [1]-[7].
3. Identify a concrete research gap in how existing work integrates capability with reliability governance.
4. Propose a reliability-oriented Agentic AI architecture that separates planning from execution and
   pre-action risk screening from post-action verification, with bounded human-in-the-loop approval.
5. Demonstrate the proposed control loop end-to-end through a small, safe, non-destructive prototype.

### 3.3 Problem Statement
Existing research treats planning, memory and retrieval, tool use, multi-agent collaboration, and
security/privacy risk as largely separate concerns, addressed in isolation across different surveys and
systems [1][2][3][5][6]. A practical gap remains in integrating these capabilities into a minimal,
teachable reference architecture that combines pre-action risk assessment, bounded human oversight, and
post-action verification in one demonstrable control loop — one that a T.E.-level student can understand,
diagram, and implement as a small working prototype. This seminar addresses that gap by proposing such an
architecture and validating its feasibility through a structural evaluation framework and a demonstrable
prototype, rather than isolated capability benchmarks.

*(Phase 2 correction: the earlier draft asserted "there is no widely taught, minimal reference
architecture that integrates..." — an absolute, unfalsifiable negative-existence claim. Replaced with the
defensible "a practical gap remains in integrating..." formulation, which claims only what the literature
review actually supports.)*

---

## 4. RELATED WORK / LITERATURE SURVEY

| # | Author(s), Year | Venue | Contribution | Relevance / Limitation |
|---|---|---|---|---|
| [1] | Acharya, Kuppan & Divya, 2025 | IEEE Access | Comprehensive survey defining Agentic AI, its characteristics and methodologies | Broad framing; does not propose a concrete reliability-oriented control loop |
| [2] | Dong et al., 2024 | IEEE AIoTC Conf. | Frames the LLM as a general-purpose controller over perception, memory, planning, action | Theoretical/technological survey; limited treatment of pre-action safety |
| [3] | Wang et al., 2024 | Frontiers of Computer Science | Unified construction framework for LLM-based autonomous agents; applications across domains | Strong architectural framing; verification/human oversight not a central axis |
| [4] | Yao et al., 2023 | ICLR | ReAct: interleaves reasoning traces with actions in a single loop | Core mechanism reused in our Reasoning/Planning stage; no built-in risk gating |
| [5] | Li et al., 2024 | Vicinagearth | Surveys LLM-based multi-agent systems: workflow, infrastructure, challenges | Scopes to multi-agent coordination; this seminar deliberately scopes to a single agent's reliability loop |
| [6] | Gan et al., 2026 | ACM TOSEM | Taxonomy of security and privacy threats in LLM-based agents | Motivates our pre-action risk gate and human-in-the-loop step; a threat catalog, not a control-loop design |
| [7] | Lewis et al., 2020 | NeurIPS | Retrieval-Augmented Generation (RAG): couples a parametric generator with a non-parametric retriever | Basis for the Memory + RAG block in the proposed architecture |

**Synthesis:** [1]-[3] establish *what* an agentic system is and *how* its components fit together;
[4] and [7] supply the two concrete mechanisms (reasoning-acting interleaving; retrieval grounding) most
seminars and prototypes build on; [5] shows the field's move toward multi-agent orchestration, which this
seminar intentionally does not chase, in favor of getting a single agent's reliability loop right first;
[6] shows *why* reliability governance is not optional once such loops are deployed. None of [1]-[7]
integrate pre-action risk gating and post-action verification into one minimal, demonstrable loop — the
gap this seminar targets.

---

## 5. RESEARCH GAP
(see 03_RESEARCH/LITERATURE.md "Research Gap" section for the fully worded, citation-grounded version —
reproduced here for the PPT/synopsis body)

> Existing research addresses planning, memory, retrieval, tool use, multi-agent collaboration, and
> security/privacy risk as individual, separately-studied components [1]-[3][5][6]. A practical gap
> remains in integrating these capabilities into a minimal, teachable reference architecture that
> combines pre-action risk assessment, bounded human oversight, and post-action verification in one
> demonstrable control loop that a student can build and demonstrate.

---

## 6. PROPOSED METHODOLOGY / ARCHITECTURE

### 6.1 Architecture (top-to-bottom control flow)
```
User Goal
   -> Goal Analyzer (interpret intent, extract constraints)
   -> Reasoning Engine / LLM (ReAct-style reasoning [4])
   -> Task Decomposition (break goal into ordered subtasks)
   -> Planner (sequence subtasks, choose next action)
   -> Memory + RAG [7] (retrieve relevant context/knowledge)
   -> Tool / API Manager (select the right tool for the action)
   -> Risk & Permission Gate (classify action risk: low / high)
        -> [high risk] Human Approval  --(denied)--> Terminate safely, log reason
        -> [approved or low risk] proceed
   -> Execution (perform the action via the selected tool)
   -> Observation (capture the actual result/state)
   -> Verification (check result against expected outcome/goal)
        -> [fail, retries remain] Replanning / Retry -> back to Planner
        -> [fail, retries exhausted] Escalate to human / terminate safely
        -> [pass] continue
   -> Aggregate Verified Outputs
   -> Final Result to User
```
**Key design separations (must be visually explicit in the diagram):**
- **Planning vs. Execution:** everything above "Risk & Permission Gate" decides *what to do*; everything
  from "Execution" onward *does it*. These are drawn as two visually distinct zones.
- **Pre-action safety vs. post-action verification:** the Risk & Permission Gate (with human approval)
  sits *before* Execution; Verification sits *after* Observation. Human approval never occurs after a
  risky action has already run.

Source: Author's proposed architecture, synthesized from the component vocabulary in [1], [2], [4], [7]
and the risk taxonomy in [6]. This is an original diagram for this seminar, not reproduced from any
single source.

### 6.2 Bounded Agent Algorithm

```
ALGORITHM: BoundedAgenticLoop(goal, MAX_RETRIES)
1.  understand(goal) -> intent, constraints
2.  subtasks <- decompose(intent)
3.  plan <- generate_plan(subtasks)
4.  FOR each step in plan:
5.      context <- retrieve(step, memory, knowledge_base)      # RAG [7]
6.      tool <- select_tool(step, context)
7.      risk <- assess_risk(tool, step)
8.      IF risk == HIGH:
9.          approved <- request_human_approval(step, tool)
10.         IF NOT approved:
11.             terminate_safely(reason="denied by user"); RETURN partial_result
12.     result <- execute(tool, step)
13.     observation <- observe(result)
14.     verified <- verify(observation, expected(step))
15.     retries <- 0
16.     WHILE NOT verified AND retries < MAX_RETRIES:
17.         step <- replan(step, observation)
18.         result <- execute(select_tool(step, context), step)
19.         observation <- observe(result)
20.         verified <- verify(observation, expected(step))
21.         retries <- retries + 1
22.     IF NOT verified:
23.         escalate_to_human(step, observation); RETURN partial_result
24.     append(observation, verified_outputs)
25. RETURN aggregate(verified_outputs)
```
The `WHILE` loop is explicitly bounded by `MAX_RETRIES` (line 16) — the loop provably terminates, so an
infinite retry loop is not possible by construction.

### 6.3 Conceptual Prototype (Phase 3, built only after PPT/synopsis approval)
A minimal Python implementation demonstrating: goal understanding -> task decomposition -> planning ->
tool selection -> execution -> observation -> verification -> bounded retry -> final response, using
safe, non-destructive tools (e.g., a calculator tool, a mock document/task-lookup tool, a small local
RAG index over a handful of text files) and one deliberately "high-risk" mock action that triggers the
human-approval gate. No file deletion, no network write actions to third-party services, no financial or
credential operations.

---

## 7. HARDWARE / SOFTWARE SPECIFICATION

**Hardware:** standard laptop/desktop (CPU sufficient for the prototype's scale), 8GB+ RAM recommended,
internet connectivity for LLM API calls; GPU not required for the scope of this seminar's prototype.

**Software:** Python 3.x; an LLM API (used only for the Phase 3 prototype, not claimed elsewhere);
a lightweight agent-orchestration approach (hand-rolled loop, or LangChain/LangGraph-style tool-calling
if used in the prototype — to be stated accurately once Phase 3 is built, not claimed in advance);
a small local vector store / simple retrieval mechanism for the RAG component; Git/GitHub for version
control; VS Code as the editor; a web browser for any API-based tool calls in the demo.

*(Note: this list states what the prototype is planned to use. The synopsis/PPT will only assert a
technology was "used" once Phase 3 actually uses it — see master instruction's no-false-claims rule.)*

---

## 8. EVALUATION FRAMEWORK (proposed / expected — no fabricated results)

Since no experiment has yet been run, the seminar presents these as **proposed evaluation metrics** to
assess the architecture once the Phase 3 prototype exists, phrased with "evaluate / assess / investigate,"
never with invented percentages:

| Metric | What it would assess |
|---|---|
| Task Success Rate | Whether the agent reaches the user's goal within the bounded loop |
| Planning Accuracy | Whether decomposed subtasks are correct/sufficient for the goal |
| Tool-Call Success Rate | Whether the correct tool is selected and invoked without error |
| Retrieval / Knowledge Grounding | Whether retrieved context is relevant to the current subtask |
| Verification Success Rate | Whether the verification step correctly accepts/rejects outcomes |
| Execution Time | Wall-clock time per goal, per retry |
| Human Intervention Rate | Fraction of actions routed to the human-approval gate |
| Safety Violation Rate | Count of actions that would have bypassed the risk gate if it were absent |

---

## 9. APPLICATIONS
- Autonomous coding assistants that plan multi-file changes, run tests, and verify results before
  presenting a diff.
- Enterprise workflow copilots that read documents, query internal systems, and draft actions (e.g.,
  ticket triage) with human approval for anything customer-facing.
- Research assistants that retrieve literature (RAG), synthesize findings, and flag claims needing
  human verification.
- Personal task agents (scheduling, form-filling, data lookup) where irreversible actions (payments,
  sending messages) are always gated behind explicit user approval.

## 10. CHALLENGES AND LIMITATIONS
- Reliable risk classification (what counts as "high-risk") is context-dependent and not solved by a
  fixed rule set alone [6].
- Verification is only as good as the specification of "expected outcome" — ambiguous goals make
  automatic verification hard.
- Latency/cost overhead from retrieval, multiple LLM calls, and human-approval pauses.
- Multi-agent extensions (per [5]) introduce coordination and trust issues beyond this seminar's
  single-agent scope.
- This seminar's own evaluation is structural/qualitative (Section 8), not a controlled experiment —
  a stated limitation, not a hidden one.

## 11. CONCLUSION AND FUTURE WORK
Agentic AI extends LLMs from single-turn generation to autonomous, multi-step, goal-directed behavior by
combining planning, memory/retrieval, tool use, and verification in a loop [1][2][3][4][7]. This seminar
identified a gap in how existing work integrates that capability with reliability governance, and
proposed an architecture that explicitly separates planning from execution and pre-action risk screening
from post-action verification, with bounded human-in-the-loop approval and a retry-bounded verification
loop. Future work includes building out the Phase 3 prototype fully, extending the architecture to
multi-agent settings [5] while preserving the same reliability guarantees, and empirically evaluating the
proposed metrics (Section 8) once a working system exists.

## 12. REFERENCES
See 03_RESEARCH/LITERATURE.md for full verified citations [1]-[7]; formatted per template's numbered
IEEE-style bracket format in the final documents.
