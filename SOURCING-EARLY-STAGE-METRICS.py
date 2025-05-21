import streamlit as st
import pandas as pd
import plotly.express as px
import re
import numpy as np


import streamlit as st
import pandas as pd

# Custom colors
custom_colors = ["#2F76B9", "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00", "#B4BBBE", "#e6657b", "#026df5", "#5aede2"]

# Load the CSV file
df = pd.read_csv("SOURCING & EARLY STAGE METRICS.csv")

# Convert specified columns to datetime
df['INVITATIONDT'] = pd.to_datetime(df['INVITATIONDT'], errors='coerce')
df['ACTIVITY_CREATED_AT'] = pd.to_datetime(df['ACTIVITY_CREATED_AT'], errors='coerce')
df['INSERTEDDATE'] = pd.to_datetime(df['INSERTEDDATE'], errors='coerce')

# Section heading
st.markdown(f"## <span style='color:{custom_colors[0]};'>Application to Unresponsive Folder</span>", unsafe_allow_html=True)

# --- Filters ---
with st.expander("🔍 Apply Filters", expanded=True):

    # Date range filter for INVITATIONDT
    min_date = df['INVITATIONDT'].min()
    max_date = df['INVITATIONDT'].max()

    start_date, end_date = st.date_input(
        "Select Invitation Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Checkbox filter for WORKLOCATION
    all_locations = sorted(df['WORKLOCATION'].dropna().unique())
    selected_locations = st.multiselect("Select Work Location(s)", all_locations, default=all_locations)

    # Checkbox filter for CAMPAIGNTITLE
    all_titles = sorted(df['CAMPAIGNTITLE'].dropna().unique())
    selected_titles = st.multiselect("Select Campaign Title(s)", all_titles, default=all_titles)

# --- Apply filters ---
filtered_df = df[
    (df['INVITATIONDT'] >= pd.to_datetime(start_date)) &
    (df['INVITATIONDT'] <= pd.to_datetime(end_date)) &
    (df['WORKLOCATION'].isin(selected_locations)) &
    (df['CAMPAIGNTITLE'].isin(selected_titles))
]

# --- Logic for Unresponsive Folder ---
unresponsive_df = filtered_df[
    (filtered_df['FOLDER_FROM_TITLE'].isna() | (filtered_df['FOLDER_FROM_TITLE'].str.strip() == "")) &
    (filtered_df['FOLDER_TO_TITLE'].str.contains("Unresponsive", case=False, na=False))
]

# Count unique CAMPAIGNINVITATIONID
unique_app_count = unresponsive_df['CAMPAIGNINVITATIONID'].nunique()

# Display result as table
st.markdown("### 📊 Metrics Summary")
styled_table = pd.DataFrame({
    'Metric': ['Application to Unresponsive Folder'],
    'Count of Unique Campaign Invitations': [unique_app_count]
})

# Display table with custom color styling
st.dataframe(
    styled_table.style.applymap(lambda _: f'background-color: {custom_colors[2]}; color: black', subset=pd.IndexSlice[:, ['Metric']])
                        .applymap(lambda _: f'color: black', subset=pd.IndexSlice[:, ['Count of Unique Campaign Invitations']])
)

    
