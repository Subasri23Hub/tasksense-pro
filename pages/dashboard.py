import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from core.utils import PRIORITY_COLORS, URGENCY_COLORS, OVERLOAD_COLORS, get_category_icon


def render_dashboard(result):
    """Render the full analytics dashboard."""

    st.markdown('<div class="section-header">📊 Analytics Dashboard</div>', unsafe_allow_html=True)

    tasks = result.tasks
    if not tasks:
        st.info("No tasks to display analytics for.")
        return

    # ── Data Prep ────────────────────────────────────────────────
    df = pd.DataFrame([t.model_dump() for t in tasks])

    # ── Row 1: Category Breakdown ──────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        cat_counts = df["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig_cat = px.pie(
            cat_counts,
            values="Count",
            names="Category",
            title="Tasks by Category",
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_cat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            title_font_size=14,
            showlegend=True,
            legend=dict(font=dict(color="#94a3b8", size=11)),
            margin=dict(t=40, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        pri_counts = df["priority_bucket"].value_counts().reset_index()
        pri_counts.columns = ["Priority", "Count"]
        pri_order = ["Do Now", "Do Today", "Schedule Soon", "Postpone", "Delegate"]
        color_map = {k: v for k, v in PRIORITY_COLORS.items()}
        fig_pri = px.bar(
            pri_counts,
            x="Priority",
            y="Count",
            title="Priority Distribution",
            color="Priority",
            color_discrete_map=color_map,
        )
        fig_pri.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            title_font_size=14,
            showlegend=False,
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            margin=dict(t=40, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_pri, use_container_width=True)

    # ── Row 2: Urgency + Effort ──────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        urg_counts = df["urgency"].value_counts().reset_index()
        urg_counts.columns = ["Urgency", "Count"]
        fig_urg = px.pie(
            urg_counts,
            values="Count",
            names="Urgency",
            title="Urgency Breakdown",
            hole=0.5,
            color="Urgency",
            color_discrete_map={"high": "#FF4B4B", "medium": "#FFA500", "low": "#21C55D"},
        )
        fig_urg.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            title_font_size=14,
            showlegend=True,
            legend=dict(font=dict(color="#94a3b8", size=11)),
            margin=dict(t=40, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_urg, use_container_width=True)

    with col4:
        effort_order = ["10 min", "30 min", "1 hour", "2 hours", "3+ hours"]
        eff_counts = df["effort"].value_counts().reindex(effort_order, fill_value=0).reset_index()
        eff_counts.columns = ["Effort", "Count"]
        fig_eff = px.bar(
            eff_counts,
            x="Effort",
            y="Count",
            title="Effort Distribution",
            color="Count",
            color_continuous_scale="Purples",
        )
        fig_eff.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            title_font_size=14,
            showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            margin=dict(t=40, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_eff, use_container_width=True)

    # ── Row 3: Task Table ────────────────────────────────────
    st.markdown('<div class="section-header">📋 Full Task Table</div>', unsafe_allow_html=True)
    display_df = df[["task", "category", "deadline_text", "normalized_deadline",
                      "urgency", "importance", "effort", "priority_bucket"]].copy()
    display_df.columns = ["Task", "Category", "Deadline (Raw)", "Deadline (Date)",
                           "Urgency", "Importance", "Effort", "Priority"]
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )
