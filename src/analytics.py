import os
import sqlite3
import pandas as pd
import streamlit as st


def load_data(db_url: str) -> pd.DataFrame:
    try:
        with sqlite3.connect(db_url) as conn:
            return pd.read_sql_query(
                "SELECT * FROM leads",
                conn
            )

    except Exception as e:
        st.error(
            f"Database connection failed: {e}"
        )
        st.stop()


def render_dashboard() -> None:

    st.set_page_config(
        page_title="AcademyOps Dashboard",
        page_icon="🚀",
        layout="wide"
    )

    st.title("🚀 AcademyOps Dashboard")
    st.write("Live Funnel Analytics")

    db_url = os.getenv(
        "DATABASE_URL",
        "academyops.db"
    )

    df = load_data(db_url)

    st.subheader("All Leads")
    st.dataframe(df)

    if df.empty:
        st.warning(
            "No leads found in the database."
        )
        return

    st.subheader(
        "Pipeline Stage Distribution"
    )

    stage_order = [
        "New",
        "Contacted",
        "Qualified",
        "Demo",
        "Enrolled",
        "Lost"
    ]

    counts = (
        df["stage"]
        .value_counts()
        .reindex(
            stage_order,
            fill_value=0
        )
        .reset_index()
    )

    counts.columns = [
        "Stage",
        "Count"
    ]

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Raw Data")
        st.dataframe(
            counts,
            width="stretch"
        )

    with col2:
        st.markdown("### Visual Funnel")

        chart_data = counts.set_index(
            "Stage"
        )

        st.bar_chart(
            chart_data
        )


if __name__ == "__main__":
    render_dashboard()