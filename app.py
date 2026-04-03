import streamlit as st
import json
from pathlib import Path

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TaskSense Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ──────────────────────────────────────────────────────────────────
css_path = Path(__file__).parent / "assets" / "styles.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Imports ───────────────────────────────────────────────────────────────────
from core.planner import run_planner, run_followup
from core.utils import (
    get_urgency_badge, get_priority_emoji, get_category_icon,
    mode_emoji, PRIORITY_COLORS, OVERLOAD_COLORS, effort_to_hours
)
from pages.dashboard import render_dashboard
from pages.settings import render_settings

# ── Session State Init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "result": None,
        "raw_json": None,
        "user_input": "",
        "mode": "Work Mode",
        "available_hours": 8,
        "followup_history": [],
        "active_tab": "Planner",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Sample Inputs ─────────────────────────────────────────────────────────────
SAMPLE_INPUTS = {
    "Work Mode": "Finish the project proposal by EOD, call the client at 3pm today, review team pull requests before standup, reply to HR about the offer letter, prepare slides for Friday's all-hands meeting, update the Jira board, send weekly report to manager by Thursday.",
    "Student Mode": "Submit the economics assignment by Friday, study chapters 5 and 6 for Monday exam, attend lab session tomorrow at 2pm, buy stationery, call mom this weekend, finish reading the case study, register for next semester courses before the deadline.",
    "Interview Prep Mode": "Research company background and values, update resume with recent project, practice 10 behavioral questions today, prepare answers for system design round, do a mock interview with a friend this week, review data structures, finalize portfolio link.",
    "Exam Week Mode": "Revise thermodynamics chapters 1-4, solve 3 past papers in maths, submit pending lab report by tonight, get enough sleep, revise organic chemistry reactions, do a full mock test tomorrow, review notes from last week.",
    "Personal Life Mode": "Renew driving license before the 10th, buy groceries, pay electricity bill, call dentist for appointment, book train tickets for next weekend, clean the house, return the library books.",
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 TaskSense Pro")
    st.markdown("---")

    mode = st.selectbox(
        "Planning Mode",
        ["Work Mode", "Student Mode", "Interview Prep Mode", "Exam Week Mode", "Personal Life Mode"],
        index=["Work Mode", "Student Mode", "Interview Prep Mode", "Exam Week Mode", "Personal Life Mode"].index(
            st.session_state["mode"]
        ),
    )
    st.session_state["mode"] = mode
    st.markdown(f"**Active:** {mode_emoji(mode)} {mode}")

    st.markdown("---")

    available_hours = st.slider(
        "⏰ Available Hours Today",
        min_value=1, max_value=16,
        value=st.session_state["available_hours"],
        step=1,
    )
    st.session_state["available_hours"] = available_hours

    st.markdown("---")

    active_tab = st.radio(
        "Navigate",
        ["🗓️ Planner", "📊 Dashboard", "⚙️ Settings"],
        index=["🗓️ Planner", "📊 Dashboard", "⚙️ Settings"].index(
            f"{'🗓️ Planner' if st.session_state['active_tab'] == 'Planner' else ('📊 Dashboard' if st.session_state['active_tab'] == 'Dashboard' else '⚙️ Settings')}"
        ),
    )
    st.session_state["active_tab"] = active_tab.split(" ", 1)[1]

    if st.session_state["result"]:
        st.markdown("---")
        st.markdown("### 📌 Session Summary")
        r = st.session_state["result"]
        st.metric("Tasks", r.summary.total_tasks)
        st.metric("Urgent", r.summary.urgent_tasks)
        st.metric("Est. Hours", f"{r.summary.estimated_hours:.1f}h")
        overload = r.summary.overload_risk
        color = OVERLOAD_COLORS.get(overload, "#94a3b8")
        st.markdown(
            f'<div style="color:{color};font-weight:600;font-size:0.85rem;">⚠️ Overload: {overload.upper()}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        if st.button("🗑️ Clear Session"):
            st.session_state["result"] = None
            st.session_state["raw_json"] = None
            st.session_state["followup_history"] = []
            st.rerun()

# ── SETTINGS PAGE ─────────────────────────────────────────────────────────────
if st.session_state["active_tab"] == "Settings":
    render_settings()
    st.stop()

# ── DASHBOARD PAGE ────────────────────────────────────────────────────────────
if st.session_state["active_tab"] == "Dashboard":
    if st.session_state["result"]:
        render_dashboard(st.session_state["result"])
    else:
        st.markdown('<div class="section-header">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
        st.info("Run the planner first to see analytics.")
    st.stop()

# ── PLANNER PAGE ──────────────────────────────────────────────────────────────
st.markdown('<div class="app-title">🧠 TaskSense Pro</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Paste your messy notes → get a prioritized, deadline-aware execution plan</div>',
    unsafe_allow_html=True,
)

# ── Input Section ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📝 Input Your Tasks</div>', unsafe_allow_html=True)

col_input, col_sample = st.columns([5, 1])
with col_sample:
    if st.button("📋 Load Sample", use_container_width=True):
        st.session_state["user_input"] = SAMPLE_INPUTS.get(mode, "")

user_input = st.text_area(
    "Paste tasks, notes, reminders, or anything messy",
    value=st.session_state["user_input"],
    height=160,
    placeholder="e.g. Call HR today, submit assignment by Friday, prepare interview this week, buy groceries, renew passport before Monday...",
    label_visibility="collapsed",
)
st.session_state["user_input"] = user_input

btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 4])
with btn_col1:
    analyze_clicked = st.button("⚡ Analyze & Plan", use_container_width=True, type="primary")
with btn_col2:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state["result"] = None
        st.session_state["raw_json"] = None
        st.session_state["user_input"] = ""
        st.session_state["followup_history"] = []
        st.rerun()

# ── Run Planner ───────────────────────────────────────────────────────────────
if analyze_clicked:
    if not user_input.strip():
        st.warning("Please enter some tasks or notes first.")
    else:
        with st.spinner("🧠 Analyzing your tasks with AI... (this may take 15–30 seconds)"):
            result, raw = run_planner(
                user_input=user_input,
                mode=mode,
                available_hours=available_hours,
            )
        if result is None:
            st.error(f"Something went wrong:\n\n{raw}")
        else:
            st.session_state["result"] = result
            st.session_state["raw_json"] = raw
            st.session_state["followup_history"] = []
            st.success("✅ Plan generated successfully!")

# ── Results ───────────────────────────────────────────────────────────────────
result = st.session_state.get("result")

if result:
    st.markdown("---")

    # ── Summary Cards ─────────────────────────────────────────
    st.markdown('<div class="section-header">📈 Summary</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)

    def metric_card(col, value, label):
        col.markdown(
            f'<div class="metric-card"><div class="metric-value">{value}</div><div class="metric-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    metric_card(c1, result.summary.total_tasks, "Total Tasks")
    metric_card(c2, result.summary.urgent_tasks, "Urgent")
    metric_card(c3, result.summary.high_priority_tasks, "Do Now")
    metric_card(c4, f"{result.summary.estimated_hours:.1f}h", "Est. Hours")
    overload_risk = result.summary.overload_risk
    overload_color = {"low": "#21C55D", "medium": "#FFA500", "high": "#FF4B4B"}.get(overload_risk, "#94a3b8")
    c5.markdown(
        f'<div class="metric-card"><div class="metric-value" style="color:{overload_color};">{overload_risk.upper()}</div><div class="metric-label">Overload Risk</div></div>',
        unsafe_allow_html=True,
    )

    # ── Overload Banner ───────────────────────────────────────
    css_class = f"overload-{result.summary.overload_risk}"
    icon = {"low": "✅", "medium": "⚠️", "high": "🚨"}.get(result.summary.overload_risk, "ℹ️")
    st.markdown(
        f'<div class="{css_class}">{icon} {result.summary.overload_message}</div>',
        unsafe_allow_html=True,
    )

    # ── Tabs: Priority Buckets | Daily Plan | Insights ────────
    tab1, tab2, tab3 = st.tabs(["🎯 Priority Buckets", "🗓️ Daily Plan", "💡 Insights & Warnings"])

    # TAB 1 — Priority Buckets
    with tab1:
        buckets = ["Do Now", "Do Today", "Schedule Soon", "Postpone", "Delegate"]
        bucket_tasks = {b: [t for t in result.tasks if t.priority_bucket == b] for b in buckets}

        cols = st.columns(len(buckets))
        for col, bucket in zip(cols, buckets):
            tasks_in_bucket = bucket_tasks[bucket]
            emoji = get_priority_emoji(bucket)
            color = PRIORITY_COLORS[bucket]
            with col:
                st.markdown(
                    f'<div style="color:{color};font-weight:700;font-size:0.85rem;text-transform:uppercase;'
                    f'letter-spacing:1px;margin-bottom:0.7rem;padding-bottom:0.4rem;'
                    f'border-bottom:2px solid {color}40;">{emoji} {bucket} ({len(tasks_in_bucket)})</div>',
                    unsafe_allow_html=True,
                )
                if not tasks_in_bucket:
                    st.markdown('<div style="color:#4b5563;font-size:0.8rem;font-style:italic;">No tasks</div>', unsafe_allow_html=True)
                for t in tasks_in_bucket:
                    icon = get_category_icon(t.category)
                    urg_dot = get_urgency_badge(t.urgency)
                    st.markdown(
                        f"""
                        <div class="task-card">
                            <div class="task-card-title">{icon} {t.task}</div>
                            <div class="task-card-meta">
                                <span class="badge badge-{t.urgency}">{urg_dot} {t.urgency}</span>
                                <span class="badge" style="background:rgba(255,255,255,0.05);color:#94a3b8;border:1px solid rgba(255,255,255,0.1);">⏱ {t.effort}</span>
                                <span class="badge" style="background:rgba(255,255,255,0.05);color:#94a3b8;border:1px solid rgba(255,255,255,0.1);">📅 {t.deadline_text}</span>
                            </div>
                            <div class="task-card-reason">💬 {t.reason}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # TAB 2 — Daily Plan
    with tab2:
        st.markdown('<div class="section-header">🗓️ Your Execution Plan for Today</div>', unsafe_allow_html=True)
        plan_blocks = [
            ("🌅 Morning", result.daily_plan.morning, "#f59e0b"),
            ("☀️ Afternoon", result.daily_plan.afternoon, "#3b82f6"),
            ("🌙 Evening", result.daily_plan.evening, "#8b5cf6"),
        ]
        for title, items, color in plan_blocks:
            st.markdown(
                f'<div class="plan-block">'
                f'<div class="plan-block-title" style="color:{color};">{title}</div>',
                unsafe_allow_html=True,
            )
            if items:
                for item in items:
                    st.markdown(
                        f'<div class="plan-item">▸ {item}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown('<div style="color:#4b5563;font-size:0.85rem;font-style:italic;padding:0.4rem 0;">Nothing scheduled</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # TAB 3 — Insights
    with tab3:
        if result.warnings:
            st.markdown('<div class="section-header">⚠️ Warnings</div>', unsafe_allow_html=True)
            for w in result.warnings:
                st.markdown(f'<div class="warning-box">⚠️ {w}</div>', unsafe_allow_html=True)

        if result.recommendations:
            st.markdown('<div class="section-header">💡 Recommendations</div>', unsafe_allow_html=True)
            for r_item in result.recommendations:
                st.markdown(f'<div class="rec-box">✦ {r_item}</div>', unsafe_allow_html=True)

        if not result.warnings and not result.recommendations:
            st.success("No major issues detected. Your plan looks solid!")

    # ── Follow-Up Section ──────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header">💬 Refine Your Plan</div>', unsafe_allow_html=True)

    followup_suggestions = [
        "Make this a 2-hour plan",
        "Only show urgent tasks",
        "Focus on work tasks only",
        "What can I postpone?",
        "Give me tomorrow's plan",
        "Reduce overload",
    ]
    st.markdown("**Quick refine:**")
    cols_q = st.columns(len(followup_suggestions))
    for col, suggestion in zip(cols_q, followup_suggestions):
        if col.button(suggestion, key=f"quick_{suggestion}", use_container_width=True):
            st.session_state["followup_input"] = suggestion

    followup_input = st.text_input(
        "Or type your own request",
        value=st.session_state.get("followup_input", ""),
        placeholder="e.g. Make this a 3-hour plan, focus on study tasks, what should I do first?",
        key="followup_text",
    )

    if st.button("🔄 Refine Plan", type="primary"):
        query = followup_input.strip() or st.session_state.get("followup_input", "")
        if not query:
            st.warning("Please type a refinement request.")
        else:
            with st.spinner("🔄 Refining your plan..."):
                new_result, new_raw = run_followup(
                    existing_plan_json=st.session_state["raw_json"],
                    followup_request=query,
                    mode=mode,
                )
            if new_result is None:
                st.error(f"Refinement failed:\n\n{new_raw}")
            else:
                st.session_state["followup_history"].append({
                    "request": query,
                    "result": new_result,
                })
                st.session_state["result"] = new_result
                st.session_state["raw_json"] = new_raw
                st.session_state["followup_input"] = ""
                st.success("✅ Plan refined!")
                st.rerun()

    # ── Follow-Up History ──────────────────────────────────────
    if st.session_state.get("followup_history"):
        with st.expander(f"📜 Refinement History ({len(st.session_state['followup_history'])} items)"):
            for i, entry in enumerate(reversed(st.session_state["followup_history"]), 1):
                st.markdown(f"**{i}.** _{entry['request']}_")
