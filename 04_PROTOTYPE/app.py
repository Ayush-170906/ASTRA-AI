"""Agentic AI Reliability Loop -- Streamlit dashboard (PRD section 10-11).

Run with:  streamlit run app.py
"""
from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from agent.state import AgentState, AgentStatus
from agent.controller import Dependencies, start, run_until_pause
from agent.demo import run_full_demo
from llm import get_llm_provider
from rag.retriever import Retriever
from tools.registry import ToolRegistry
from tools.calculator import calculate_capacity_tool
from tools.knowledge_lookup import build_search_knowledge_tool, generate_checklist_tool
from tools.mock_notification import mock_send_announcement_tool, get_sent_log

KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"
HERO_IMAGE = Path(__file__).resolve().parent / "assets" / "human-robot-hands.jpg"
VOICE_COMPONENT_DIR = Path(__file__).resolve().parent / "ui" / "voice_assistant"

st.set_page_config(page_title="Agentic AI Reliability Loop", layout="wide")


@st.cache_resource
def build_dependencies() -> Dependencies:
    retriever = Retriever(KNOWLEDGE_DIR)
    registry = ToolRegistry()
    registry.register(calculate_capacity_tool)
    registry.register(generate_checklist_tool)
    registry.register(build_search_knowledge_tool(retriever.retrieve))
    registry.register(mock_send_announcement_tool)
    llm = get_llm_provider()
    return Dependencies(llm=llm, retriever=retriever, registry=registry)


deps = build_dependencies()
voice_assistant_component = components.declare_component(
    "astra_voice_assistant", path=str(VOICE_COMPONENT_DIR)
)

if "state" not in st.session_state:
    st.session_state.state = AgentState()

state: AgentState = st.session_state.state

STAGE_ORDER = ["GOAL", "DECOMPOSE", "PLAN", "RETRIEVE", "TOOL_SELECT", "RISK_CHECK",
               "HUMAN_APPROVAL", "EXECUTE", "OBSERVE", "VERIFY"]

STATUS_ICON = {"OK": "✅", "PASS": "✅", "FAILED": "❌", "FAIL": "❌",
               "ERROR": "🛑", "ESCALATED": "🚨", "WAITING": "⏳", "DENIED": "🚫",
               "APPROVED": "✅"}


def render_trace(execution_trace) -> None:
    """Shared renderer for one AgentState's execution trace -- used by both
    Manual Mode's live trace and each Demo Mode scenario's trace below, so
    the two never drift out of sync with each other."""
    if not execution_trace:
        st.info("No run yet.")
        return
    for event in execution_trace:
        icon = STATUS_ICON.get(event.status, "•")
        line = f"**[{event.step:02d}] {event.stage}** {icon}  {event.description}"
        if event.tool:
            line += f"  ·  tool=`{event.tool}`"
        if event.risk:
            line += f"  ·  risk=`{event.risk}`"
        st.markdown(line)
        if event.result:
            st.caption(event.result)


# ------------------------------------------------------------------ styling
image_data = base64.b64encode(HERO_IMAGE.read_bytes()).decode("ascii")
st.markdown(
    f"""<style>
    .stApp {{
        background-image: linear-gradient(rgba(5, 8, 14, .78), rgba(5, 8, 14, .91)),
                          url("data:image/jpeg;base64,{image_data}");
        background-position: center center;
        background-size: cover;
        background-attachment: fixed;
        color: #f3f5f8;
    }}
    [data-testid="stHeader"] {{ background: rgba(5, 8, 14, .25); }}
    [data-testid="stMain"] {{ background: transparent; }}
    [data-testid="stSidebar"] {{ background: rgba(9, 13, 21, .88); }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(12, 17, 27, .76);
        border: 1px solid rgba(255, 255, 255, .12);
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }}
    h1, h2, h3 {{ letter-spacing: -.025em; }}
    .eyebrow {{ color: #b8c6d8; font-size: .78rem; letter-spacing: .12em;
                font-weight: 700; text-transform: uppercase; }}
    .step-card {{ background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.12);
                  border-radius: 12px; padding: .75rem 1rem; margin: .35rem 0 1rem; }}
    .step-label {{ color: #9eacc0; font-size: .72rem; text-transform: uppercase;
                   letter-spacing: .1em; }}
    .step-value {{ color: #f8fafc; font-size: 1rem; font-weight: 650; margin-top: .15rem; }}
    div.stButton > button[kind="primary"] {{ border-radius: 10px; min-height: 3rem;
        font-weight: 700; border: 0; background: linear-gradient(100deg, #77d2ff, #9e9bff);
        color: #111827; }}
    div.stButton > button {{ border-radius: 9px; }}
    </style>""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ header
st.title("Agentic AI Reliability Loop")
st.markdown('<div class="eyebrow">Deterministic local demo · no live LLM connected</div>',
            unsafe_allow_html=True)
st.caption("Goal → Plan → Retrieve → Risk gate → Human approval → Execute → Verify")

if "last_voice_event_id" not in st.session_state:
    st.session_state.last_voice_event_id = None
if "voice_notice" not in st.session_state:
    st.session_state.voice_notice = ""
if "last_voice_transcript" not in st.session_state:
    st.session_state.last_voice_transcript = ""

voice_summary = ""
if state.final_result:
    voice_summary = state.final_result.get("final_result", "Your request is complete.")
elif state.status == AgentStatus.WAITING_FOR_APPROVAL:
    voice_summary = "Your request needs approval in Manual Mode."
elif state.status == AgentStatus.ESCALATED:
    voice_summary = "The agent stopped after retries and needs human review."
elif state.status == AgentStatus.TERMINATED:
    voice_summary = "The run was terminated after the action was denied."

voice_event = voice_assistant_component(
    workflow_status=state.status.value,
    workflow_message=voice_summary,
    default=None,
    key="astra_voice_assistant",
)
if st.session_state.voice_notice:
    st.info(st.session_state.voice_notice)

if isinstance(voice_event, dict):
    event_id = voice_event.get("id")
    if event_id and event_id != st.session_state.last_voice_event_id:
        st.session_state.last_voice_event_id = event_id
        if voice_event.get("kind") == "status":
            st.session_state.voice_notice = voice_event.get("message", "")
        elif voice_event.get("kind") == "transcript":
            transcript = str(voice_event.get("transcript", "")).strip()
            if transcript:
                st.session_state.voice_notice = ""
                st.session_state.last_voice_transcript = transcript
                st.session_state.custom_goal = transcript
                if state.status == AgentStatus.WAITING_FOR_APPROVAL:
                    st.session_state.voice_notice = (
                        "Transcript received. Resolve the pending approval before starting another goal."
                    )
                else:
                    # A fresh voice goal becomes editable first; execution remains
                    # an explicit action through the existing Manual Mode control.
                    state = AgentState()
                    st.session_state.state = state
                    st.session_state.demo_results = []
                st.rerun()

if "custom_goal" not in st.session_state:
    st.session_state.custom_goal = (
        "Prepare a brief for an upcoming technical event using the information available in the "
        "knowledge base, calculate the estimated registration capacity, and create a draft event "
        "checklist."
    )

demo_results = st.session_state.get("demo_results", [])
passed_count = sum(1 for result in demo_results if result.passed)
if state.status == AgentStatus.WAITING_FOR_APPROVAL:
    current_step = f"Approval required · {state.current_task.tool if state.current_task else 'action'}"
elif state.execution_trace:
    last_event = state.execution_trace[-1]
    if state.status == AgentStatus.COMPLETED:
        current_step = f"Complete · {last_event.stage}"
    elif state.status in (AgentStatus.ESCALATED, AgentStatus.TERMINATED):
        current_step = f"{state.status.value.title()} · {last_event.stage}"
    else:
        current_step = f"Step {last_event.step} · {last_event.stage}"
elif demo_results:
    current_step = f"Demo complete · {passed_count}/{len(demo_results)} scenarios passed"
else:
    current_step = "Ready · enter a goal or run the seminar demo"

with st.container(border=True):
    st.markdown('<div class="eyebrow">Agent Workspace</div>', unsafe_allow_html=True)
    goal_col, button_col = st.columns([4, 1.2])
    with goal_col:
        st.text_area("Custom goal", key="custom_goal", height=96)
    with button_col:
        demo_running = st.button("▶ Run Demo", type="primary", use_container_width=True)
        demo_reset = st.button("Reset results", use_container_width=True,
                               disabled=not bool(st.session_state.get("demo_results")))
    st.markdown(
        f'<div class="step-card"><div class="step-label">Current step</div>'
        f'<div class="step-value">{current_step}</div></div>',
        unsafe_allow_html=True,
    )

if demo_running:
    with st.spinner("Running the four deterministic seminar scenarios…"):
        st.session_state.demo_results = run_full_demo(deps)
    st.rerun()

if demo_reset:
    st.session_state.demo_results = []
    st.rerun()

# ------------------------------------------------------------------ demo outcome
if demo_results:
    st.subheader("Seminar demo results")
    st.success(f"{passed_count} of {len(demo_results)} scenarios passed")
    for result in demo_results:
        icon = "🟢" if result.passed else "🔴"
        outcome = (result.state.final_result or {}).get("final_result") or result.state.status.value
        st.markdown(f"{icon} **{result.name}** — {outcome}")

if state.status == AgentStatus.COMPLETED and state.final_result:
    summary = state.final_result.get("final_result") or "Goal completed and verified"
    st.subheader("Custom goal result")
    st.success(summary)
elif state.status == AgentStatus.ESCALATED:
    st.error("The agent stopped after bounded retries and escalated the unresolved task.")
elif state.status == AgentStatus.TERMINATED:
    st.warning("The run was terminated. A denied high-risk action was not executed.")

# ------------------------------------------------------------------ manual workflow
manual_open = state.status == AgentStatus.WAITING_FOR_APPROVAL
with st.expander("Manual Mode", expanded=manual_open):
    st.caption("Run a custom goal. High-risk actions pause for your approval or denial.")

    force_fail_on = st.checkbox(
        "Force verification failure (retry/escalation demonstration)", value=False,
        key="force_fail_on",
    )
    force_fail_target = st.text_input(
        "Subtask description contains", value="capacity", disabled=not force_fail_on,
        key="force_fail_target",
    )
    force_fail_count = st.number_input(
        "Forced attempts", min_value=1, max_value=5, value=2, disabled=not force_fail_on,
        key="force_fail_count",
    )
    can_start = state.status in (AgentStatus.IDLE, AgentStatus.COMPLETED,
                                 AgentStatus.ESCALATED, AgentStatus.TERMINATED)
    run_goal = st.button("Run custom goal", disabled=not can_start, key="run_custom_goal")
    if run_goal:
        state = AgentState()
        if force_fail_on:
            state.demo_force_fail_task_desc_contains = force_fail_target
            state.demo_force_fail_remaining = int(force_fail_count)
        st.session_state.state = state
        st.session_state.demo_results = []
        st.session_state.voice_notice = ""
        st.session_state.last_voice_transcript = ""
        start(state, st.session_state.custom_goal, deps)
        run_until_pause(state, deps)
        st.rerun()

    if state.status == AgentStatus.WAITING_FOR_APPROVAL:
        task = state.current_task
        tool = deps.registry.get(task.tool)
        st.warning("Human approval required", icon="⚠️")
        st.markdown(f"""
- **Action:** `{tool.name}` — {task.description}
- **Arguments:** `{task.arguments}`
- **Risk:** **{state.risk_level.value}**
- **Reason approval is required:** {tool.approval_reason}
""")
        approve_col, deny_col = st.columns(2)
        if approve_col.button("✅ Approve", type="primary", use_container_width=True):
            state.approval_status = "APPROVED"
            run_until_pause(state, deps)
            st.rerun()
        if deny_col.button("❌ Deny", use_container_width=True):
            state.approval_status = "DENIED"
            run_until_pause(state, deps)
            st.rerun()

# ------------------------------------------------------------------ technical details
with st.expander("Technical Details", expanded=False):
    st.caption(f"Manual Mode provider: **{deps.llm.name}** · deterministic fallback active; "
               "Ollama and Anthropic API were not available/configured at startup.")

    st.markdown("#### Tool registry")
    for registered_tool in deps.registry.describe_all():
        st.markdown(f"**{registered_tool['name']}** · risk `{registered_tool['risk']}`  "
                    f"\n{registered_tool['description']}")

    st.markdown("#### Manual execution trace")
    render_trace(state.execution_trace)
    if state.final_result:
        with st.expander("Manual raw JSON", expanded=False):
            st.json(state.final_result)

    for result in demo_results:
        with st.expander(f"{result.label} · {'PASSED' if result.passed else 'FAILED'}", expanded=False):
            render_trace(result.state.execution_trace)
            if result.state.final_result:
                st.json(result.state.final_result)

    if get_sent_log():
        with st.expander("Mock announcement log (nothing was ever really sent)", expanded=False):
            st.json(get_sent_log())
