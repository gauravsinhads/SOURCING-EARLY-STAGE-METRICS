import streamlit as st
import pandas as pd

# 🎨 Custom colors
custom_colors = ["#2F76B9", "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00", "#B4BBBE", "#e6657b", "#026df5", "#5aede2"]

# 📥 Load CSV
df = pd.read_csv("SOURCING & EARLY STAGE METRICS.csv")

# 🕒 Convert date columns to datetime
df['INVITATIONDT'] = pd.to_datetime(df['INVITATIONDT'], errors='coerce')
df['ACTIVITY_CREATED_AT'] = pd.to_datetime(df['ACTIVITY_CREATED_AT'], errors='coerce')
df['INSERTEDDATE'] = pd.to_datetime(df['INSERTEDDATE'], errors='coerce')

# 📌 Heading
st.markdown(f"## <span style='color:{custom_colors[0]};'>Application to Unresponsive Folder</span>", unsafe_allow_html=True)

# 🔎 Filter section
with st.expander("🔍 Apply Filters", expanded=False):
    # 📅 Date filter
    min_date = df['INVITATIONDT'].min()
    max_date = df['INVITATIONDT'].max()

    start_date, end_date = st.date_input(
        "Select Invitation Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # 📍 Work Location dropdown
    work_locations = sorted(df['WORKLOCATION'].dropna().unique())
    selected_locations = st.multiselect("Select Work Location(s)", work_locations, default=work_locations)

    # 📋 Campaign Title dropdown
    campaign_titles = sorted(df['CAMPAIGNTITLE'].dropna().unique())
    selected_titles = st.multiselect("Select Campaign Title(s)", campaign_titles, default=campaign_titles)

# 🔄 Apply filters
filtered_df = df[
    (df['INVITATIONDT'] >= pd.to_datetime(start_date)) &
    (df['INVITATIONDT'] <= pd.to_datetime(end_date)) &
    (df['WORKLOCATION'].isin(selected_locations)) &
    (df['CAMPAIGNTITLE'].isin(selected_titles))
]

# 📂 Filter for 'Application to Unresponsive Folder'
unresponsive_df = filtered_df[
    (filtered_df['FOLDER_FROM_TITLE'].isna() | (filtered_df['FOLDER_FROM_TITLE'].str.strip() == "")) &
    (filtered_df['FOLDER_TO_TITLE'].str.contains("Unresponsive", case=False, na=False))
]

# 📈 Metrics Calculation
count = unresponsive_df['CAMPAIGNINVITATIONID'].nunique()
total = filtered_df['CAMPAIGNINVITATIONID'].nunique()
percentage = round((count / total) * 100, 2) if total else 0.0

# 📊 Create summary DataFrame
summary_df = pd.DataFrame({
    'Metric': ['Application to Unresponsive Folder'],
    'Count': [count],
    'Percentage(%)': [percentage]
})

# 🎨 Optional: Highlight count cell
def highlight_row(row):
    return ['background-color: #F5BA2E; color: black'] * len(row)

styled_df = summary_df.style.apply(highlight_row, axis=1)

# 📋 Display the final summary table
st.markdown("### 📊 Metrics Summary")
st.dataframe(styled_df)
