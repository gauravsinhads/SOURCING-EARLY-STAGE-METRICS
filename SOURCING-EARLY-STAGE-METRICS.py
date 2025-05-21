import streamlit as st
import pandas as pd

# Custom colors
custom_colors = ["#2F76B9", "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00", "#B4BBBE", "#e6657b", "#026df5", "#5aede2"]

# Load the CSV
df = pd.read_csv("SOURCING & EARLY STAGE METRICS.csv")

# Convert to datetime
df['INVITATIONDT'] = pd.to_datetime(df['INVITATIONDT'], errors='coerce')
df['ACTIVITY_CREATED_AT'] = pd.to_datetime(df['ACTIVITY_CREATED_AT'], errors='coerce')
df['INSERTEDDATE'] = pd.to_datetime(df['INSERTEDDATE'], errors='coerce')

# Header
st.markdown(f"## <span style='color:{custom_colors[0]};'>Application to Unresponsive Folder</span>", unsafe_allow_html=True)

# --- Filters ---
with st.expander("🔍 Apply Filters", expanded=False):

    # Date filter
    min_date = df['INVITATIONDT'].min()
    max_date = df['INVITATIONDT'].max()

    start_date, end_date = st.date_input(
        "Select Invitation Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Work Location Dropdown
    all_locations = sorted(df['WORKLOCATION'].dropna().unique())
    with st.expander("Select Work Location(s)"):
        selected_locations = st.multiselect("Work Location", all_locations, default=all_locations)

    # Campaign Title Dropdown
    all_titles = sorted(df['CAMPAIGNTITLE'].dropna().unique())
    with st.expander("Select Campaign Title(s)"):
        selected_titles = st.multiselect("Campaign Title", all_titles, default=all_titles)

# --- Filter the dataframe ---
filtered_df = df[
    (df['INVITATIONDT'] >= pd.to_datetime(start_date)) &
    (df['INVITATIONDT'] <= pd.to_datetime(end_date)) &
    (df['WORKLOCATION'].isin(selected_locations)) &
    (df['CAMPAIGNTITLE'].isin(selected_titles))
]

# --- Logic: Application to Unresponsive Folder ---
unresponsive_df = filtered_df[
    (filtered_df['FOLDER_FROM_TITLE'].isna() | (filtered_df['FOLDER_FROM_TITLE'].str.strip() == "")) &
    (filtered_df['FOLDER_TO_TITLE'].str.contains("Unresponsive", case=False, na=False))
]

# Count & Percentage
count_unresponsive = unresponsive_df['CAMPAIGNINVITATIONID'].nunique()
total_count = filtered_df['CAMPAIGNINVITATIONID'].nunique()
percentage = round((count_unresponsive / total_count * 100), 2) if total_count else 0.0

# --- Display Metrics Table ---
summary_df = pd.DataFrame({
    'Metric': ['Application to Unresponsive Folder', 'Percentage(%)'],
    'Count': [count_unresponsive, f"{percentage}%"]
})

st.markdown("### 📊 Metrics Summary")
st.dataframe(
    summary_df.style.applymap(lambda _: f'background-color: {custom_colors[2]}; color: black', subset=pd.IndexSlice[["Application to Unresponsive Folder"], ['Metric']])
                       .applymap(lambda _: f'color: black', subset=pd.IndexSlice[:, ['Count']])
)
