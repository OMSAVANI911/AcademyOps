import os
import sqlite3
import pandas as pd
import streamlit as st

def load_data(db_url: str) -> pd.DataFrame:
    """
    Connects to the SQLite database and retrieves all lead data.

    Args:
        db_url (str): The path or URL to the SQLite database.

    Returns:
        pd.DataFrame: A DataFrame containing the leads. Stops execution on failure.
    """
    try:
        with sqlite3.connect(db_url) as conn:
            return pd.read_sql_query("SELECT * FROM leads", conn)
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        st.stop()

def render_dashboard() -> None:
    """
    Renders the Streamlit operations dashboard, including data tables and visualizations.
    """
    # Pro-tip: Set page config makes the app look instantly more professional
    st.set_page_config(page_title="AcademyOps Dashboard", page_icon="🚀", layout="wide")
    
    st.title("🚀 AcademyOps Dashboard")
    st.write("Live Funnel Analytics")

    # 1. Securely load the database using Environment Variables
    db_url = os.getenv("DATABASE_URL", "academyops.db")
    df = load_data(db_url)

    # 2. Display the Data
    if df.empty:
        st.warning("No leads found in the database. Awaiting data ingestion.")
        return

    st.subheader("Pipeline Stage Distribution")

    # Calculate the counts safely
    stage_order = ['New', 'Contacted', 'Qualified', 'Demo', 'Enrolled', 'Lost']
    counts = df['stage'].value_counts().reindex(stage_order, fill_value=0)

    # 3. Create a clean UI using columns
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("**Raw Data**")
        st.dataframe(counts, use_container_width=True)

    with col2:
        st.markdown("**Visual Funnel**")
        st.bar_chart(counts)

if __name__ == "__main__":
    render_dashboard()