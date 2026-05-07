import streamlit as st
import pandas as pd
from utils.db import connect


def history_page():

    st.markdown("<h1>📜 Analysis History</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p>All stemness predictions made under your account.</p>",
        unsafe_allow_html=True
    )

    st.write("")

    try:
        conn = connect()

        # Use parameterised query — never f-string with user input
        df = pd.read_sql(
            "SELECT * FROM history WHERE username = ? ORDER BY date DESC",
            conn,
            params=(st.session_state.user,)
        )

        conn.close()

        if df.empty:
            st.info("ℹ️  No predictions yet. Run your first analysis from the Prediction page.")
            return

        # Rename columns for display
        df = df.rename(columns={
            "sample_name":    "Sample",
            "prediction":     "Risk Probability",
            "classification": "Stemness Score",
            "date":           "Date",
        })

        # Drop internal id / username columns from display
        display_cols = [c for c in df.columns if c not in ("id", "username")]

        st.dataframe(
            df[display_cols],
            use_container_width=True,
            hide_index=True
        )

        # Download button
        csv = df[display_cols].to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇  Download History CSV",
            data=csv,
            file_name="stemquant_history.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Could not load history: {e}")

    st.markdown(
        "<div class='sq-footer'>© 2026 StemQuant. All rights reserved.</div>",
        unsafe_allow_html=True
    )
