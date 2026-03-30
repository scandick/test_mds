from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Streamlit Showcase", page_icon="✨", layout="wide")


@st.cache_data
def load_iris() -> pd.DataFrame:
    data_path = Path(__file__).resolve().parents[2] / "data" / "Iris.csv"
    df = pd.read_csv(data_path)
    df["petal_area"] = df["PetalLengthCm"] * df["PetalWidthCm"]
    df["sepal_area"] = df["SepalLengthCm"] * df["SepalWidthCm"]
    return df


@st.cache_data
def build_timeseries(seed: int, points: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    timeline = pd.date_range("2026-01-01", periods=points, freq="D")
    base = np.linspace(20, 95, points)
    noise = rng.normal(0, 4, points).cumsum()
    trend = np.clip(base + noise, 5, None)
    return pd.DataFrame(
        {
            "date": timeline,
            "engagement": trend,
            "signups": np.clip(trend * 0.35 + rng.normal(0, 3, points), 2, None),
        }
    )


iris = load_iris()

if "likes" not in st.session_state:
    st.session_state.likes = 12
if "demo_tasks" not in st.session_state:
    st.session_state.demo_tasks = {
        "filters": True,
        "charts": True,
        "editing": False,
        "feedback": False,
    }


with st.sidebar:
    st.title("Control Room")
    species_options = sorted(iris["Species"].unique())
    selected_species = st.multiselect(
        "Species",
        species_options,
        default=species_options,
        help="Filter the dashboard to one or more flower classes.",
    )
    sample_size = st.slider("Rows in editor", 5, 30, 12)
    highlight_threshold = st.slider("Petal length focus", 1.0, 7.0, 4.7, 0.1)
    chart_mode = st.radio(
        "Comparison view",
        ("Scatter", "Box plot"),
        horizontal=True,
    )
    show_code = st.toggle("Show generated code sample", value=True)


filtered = iris[iris["Species"].isin(selected_species)].copy()
focus_count = int((filtered["PetalLengthCm"] >= highlight_threshold).sum())
timeseries = build_timeseries(seed=42, points=30)


st.title("Streamlit Capability Showcase")
st.caption(
    "One page, many use cases: dashboards, data tools, workflow UI, forms, state, "
    "chat-like blocks, downloads, and polished layouts."
)

hero_left, hero_right = st.columns((1.6, 1))

with hero_left:
    st.markdown(
        """
        ### What this page demonstrates
        - Clean dashboard composition with columns, containers and metrics
        - Interactive analytics powered by filters and cached data
        - Editable tables, downloads and lightweight workflow controls
        - UI patterns for assistants, internal tools and data apps
        """
    )

with hero_right:
    with st.container(border=True):
        st.metric("Filtered rows", len(filtered), delta=f"{len(filtered) - len(iris):+d}")
        st.metric("Focused flowers", focus_count, delta=f"threshold {highlight_threshold:.1f} cm")
        st.metric("Session likes", st.session_state.likes)


metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Species visible", filtered["Species"].nunique())
metric_2.metric("Avg petal area", f"{filtered['petal_area'].mean():.2f}")
metric_3.metric("Avg sepal area", f"{filtered['sepal_area'].mean():.2f}")
metric_4.metric("Largest petal", f"{filtered['PetalLengthCm'].max():.1f} cm")


tab_dashboard, tab_data, tab_workflow, tab_assistant = st.tabs(
    ["Analytics Dashboard", "Data Lab", "Workflow UI", "Assistant Experience"]
)


with tab_dashboard:
    chart_col, insight_col = st.columns((1.8, 1))

    with chart_col:
        st.subheader("Interactive flower analysis")
        if chart_mode == "Scatter":
            scatter = (
                alt.Chart(filtered)
                .mark_circle(size=120, opacity=0.75)
                .encode(
                    x=alt.X("SepalLengthCm", title="Sepal length (cm)"),
                    y=alt.Y("PetalLengthCm", title="Petal length (cm)"),
                    color=alt.Color("Species", legend=alt.Legend(title="Species")),
                    tooltip=[
                        "Species",
                        "SepalLengthCm",
                        "SepalWidthCm",
                        "PetalLengthCm",
                        "PetalWidthCm",
                    ],
                )
                .properties(height=420)
                .interactive()
            )
            st.altair_chart(scatter, use_container_width=True)
        else:
            box_plot = (
                alt.Chart(filtered)
                .mark_boxplot(size=44)
                .encode(
                    x=alt.X("Species", title="Species"),
                    y=alt.Y("PetalLengthCm", title="Petal length (cm)"),
                    color=alt.Color("Species", legend=None),
                )
                .properties(height=420)
            )
            st.altair_chart(box_plot, use_container_width=True)

    with insight_col:
        st.subheader("Story blocks")
        st.info(
            "Streamlit shines when you need to move quickly from idea to interactive tool "
            "without building a full frontend stack."
        )
        st.success(
            f"{focus_count} flowers currently exceed the {highlight_threshold:.1f} cm petal threshold."
        )
        with st.expander("Quick use-case ideas"):
            st.write("Internal dashboards")
            st.write("ML demo apps")
            st.write("Ops/admin control panels")
            st.write("Data exploration notebooks for non-technical users")

    trend_col, bar_col = st.columns(2)
    with trend_col:
        st.subheader("Business-style KPI chart")
        st.area_chart(timeseries.set_index("date")[["engagement", "signups"]], height=260)
    with bar_col:
        st.subheader("Species distribution")
        species_counts = filtered["Species"].value_counts().rename_axis("Species").reset_index(name="Count")
        st.bar_chart(species_counts.set_index("Species"), height=260)


with tab_data:
    st.subheader("Data editing, preview and export")
    editor_col, preview_col = st.columns((1.2, 1))

    editable = filtered.head(sample_size)[
        ["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm", "Species"]
    ]

    with editor_col:
        edited_df = st.data_editor(
            editable,
            use_container_width=True,
            num_rows="dynamic",
            hide_index=True,
            column_config={
                "Species": st.column_config.SelectboxColumn(
                    "Species",
                    options=species_options,
                    help="Switch classes to see how editing works in-place.",
                )
            },
        )
        csv_data = edited_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download edited CSV",
            data=csv_data,
            file_name="streamlit_showcase_export.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with preview_col:
        st.dataframe(
            filtered.describe(include="all"),
            use_container_width=True,
            height=320,
        )
        st.json(
            {
                "selected_species": selected_species,
                "rows_in_view": len(filtered),
                "petal_threshold": highlight_threshold,
                "mean_petal_length": round(float(filtered["PetalLengthCm"].mean()), 2),
            }
        )

    if show_code:
        st.code(
            """import streamlit as st

uploaded = st.file_uploader("Drop a CSV")
if uploaded:
    st.dataframe(uploaded)""",
            language="python",
        )


with tab_workflow:
    st.subheader("Workflow patterns for internal tools")
    left, right = st.columns((1.1, 1))

    with left:
        with st.form("launch_form", clear_on_submit=False):
            project_name = st.text_input("Project name", value="Iris Insight")
            goal = st.selectbox("Primary goal", ["Dashboard", "Monitoring", "Demo", "Backoffice"])
            include_auth = st.checkbox("Plan authentication layer")
            include_alerts = st.checkbox("Plan notifications", value=True)
            submitted = st.form_submit_button("Generate brief", use_container_width=True)

        if submitted:
            st.success(f"Brief created for {project_name}")
            st.write(
                {
                    "goal": goal,
                    "authentication": include_auth,
                    "alerts": include_alerts,
                }
            )

        progress_value = sum(st.session_state.demo_tasks.values()) / len(st.session_state.demo_tasks)
        st.progress(progress_value, text=f"Demo readiness: {progress_value:.0%}")

    with right:
        task_labels = {
            "filters": "Interactive filters are wired",
            "charts": "Charts are presentable",
            "editing": "Editing flow is approved",
            "feedback": "Stakeholder feedback is collected",
        }

        for key, label in task_labels.items():
            st.session_state.demo_tasks[key] = st.checkbox(label, value=st.session_state.demo_tasks[key])

        with st.status("Example deployment pipeline", expanded=True) as status:
            st.write("1. Load and cache source data")
            st.write("2. Render KPI blocks and charts")
            st.write("3. Accept user input through forms")
            st.write("4. Export or hand data to a downstream service")
            status.update(label="Pipeline ready to demo", state="complete")


with tab_assistant:
    st.subheader("Assistant and product-style UI")

    chat_col, action_col = st.columns((1.4, 1))

    with chat_col:
        with st.chat_message("user"):
            st.write("Show me something that feels like a lightweight AI product.")
        with st.chat_message("assistant"):
            st.write(
                "Streamlit can comfortably prototype chat tools, review workflows, "
                "knowledge assistants and guided internal copilots."
            )
            st.write("It is especially strong when speed matters more than pixel-perfect custom frontend.")

    with action_col:
        st.markdown("#### Quick reactions")
        if st.button("Like this demo", use_container_width=True):
            st.session_state.likes += 1
            st.rerun()

        mood = st.segmented_control(
            "Pick a vibe",
            options=["Business", "Playful", "Minimal"],
            default="Business",
            selection_mode="single",
        )
        st.write(f"Current vibe: **{mood}**")

        feedback = st.text_area(
            "What would you build first?",
            placeholder="Monitoring dashboard, AI helper, analytics workspace...",
        )
        if feedback:
            st.caption(f"Captured idea: {feedback}")
