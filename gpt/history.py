import streamlit as st
import pandas as pd
from utils.db import connect

def history_page():

    conn=connect()

    q=f"""
SELECT *
FROM history
WHERE username=
'{st.session_state.user}'
"""

    df=pd.read_sql(
        q,
        conn
    )

    st.title(
"Analysis History"
)

    st.dataframe(df)