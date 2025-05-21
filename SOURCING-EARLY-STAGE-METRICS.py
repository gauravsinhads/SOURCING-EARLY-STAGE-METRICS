import streamlit as st
import pandas as pd

# 🎨 Custom colors
custom_colors = ["#2F76B9", "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00", "#B4BBBE", "#e6657b", "#026df5", "#5aede2"]

# 📛 Set page title
st.set_page_config(page_title="SOURCING & EARLY STAGE METRICS", layout="wide")
st.title("📊 SOURCING & EARLY STAGE METRICS")

# 📥 Load the CSV
df = pd.read_csv("SOURCING & EARLY STAGE METRICS.csv")

# 🕒 Convert columns to datetime
df['INVITATIONDT'] = pd.to_datetime(df['INVITATIONDT'], errors='coerce')
df['ACTIVITY_CREATED_AT'] = pd.to_datetime(df['ACTIVITY_CREATED_AT'], errors='coerce')
df['INSERTEDDATE'] = pd.to_datetime(df['INSERTEDDATE'], errors='coerce')

# 🔍 Filters
with st.expander("🔎 Apply Filters", expanded=False):
    # Date range filter
    min_date = df['INVITATIONDT'].min()
    max_date = df['INVITATIONDT'].max()
    start_date, end_date = st.date_input("Select Invitation Date Range", [min_date, max_date])

    # Work Location dropdown
    work_locations = sorted(df['WORKLOCATION'].dropna().unique())
    selected_locations = st.multiselect("Select Work Location(s)", work_locations, default=work_locations)

    # Campaign Title dropdown
    campaign_titles = sorted(df['CAMPAIGNTITLE'].dropna().unique())
    selected_titles = st.multiselect("Select Campaign Title(s)", campaign_titles, default=campaign_titles)

# 🔄 Apply filters
filtered_df = df[
    (df['INVITATIONDT'] >= pd.to_datetime(start_date)) &
    (df['INVITATIONDT'] <= pd.to_datetime(end_date)) &
    (df['WORKLOCATION'].isin(selected_locations)) &
    (df['CAMPAIGNTITLE'].isin(selected_titles))
]

# 🔢 Total unique campaign invitations
total_unique_ids = filtered_df['CAMPAIGNINVITATIONID'].nunique()

# 📊 Metrics list
metrics = []

# Row 1: Application to Unresponsive Folder
count1 = filtered_df[
    (filtered_df['FOLDER_FROM_TITLE'].isna() | (filtered_df['FOLDER_FROM_TITLE'].str.strip() == "")) &
    (filtered_df['FOLDER_TO_TITLE'].str.contains("Unresponsive", case=False, na=False))
]['CAMPAIGNINVITATIONID'].nunique()
percentage1 = round((count1 / total_unique_ids) * 100, 2) if total_unique_ids else 0
metrics.append(['Application to Unresponsive Folder', count1, percentage1])

# Row 2: Unresponsive Folder to Passed MQ Folder
count2 = filtered_df[
    (filtered_df['FOLDER_FROM_TITLE'].str.strip().str.lower() == "unresponsive") &
    (filtered_df['FOLDER_TO_TITLE'].str.contains("Passed MQ", case=False, na=False))
]['CAMPAIGNINVITATIONID'].nunique()
percentage2 = round((count2 / total_unique_ids) * 100, 2) if total_unique_ids else 0
metrics.append(['Unresponsive Folder to Passed MQ Folder', count2, percentage2])

# Row 3: Unresponsive Folder to Failed MQ Folder
count3 = filtered_df[
    (filtered_df['FOLDER_FROM_TITLE'].str.strip().str.lower() == "unresponsive") &
    (filtered_df['FOLDER_TO_TITLE'].str.contains("Failed MQ", case=False, na=False))
]['CAMPAIGNINVITATIONID'].nunique()
percentage3 = round((count3 / total_unique_ids) * 100, 2) if total_unique_ids else 0
metrics.append(['Unresponsive Folder to Failed MQ Folder', count3, percentage3])

# Row 4: Unresponsive Folder to Cold Leads Folder
count4 = filtered_df[
    (filtered_df['FOLDER_FROM_TITLE'].str.strip().str.lower() == "unresponsive") &
    (filtered_df['FOLDER_TO_TITLE'].str.contains("Cold Leads", case=False, na=False))
]['CAMPAIGNINVITATIONID'].nunique()
percentage4 = round((count4 / total_unique_ids) * 100, 2) if total_unique_ids else 0
metrics.append(['Unresponsive Folder to Cold Leads Folder', count4, percentage4])

# 📋 Create summary DataFrame
summary_df = pd.DataFrame(metrics, columns=['Metric', 'Count', 'Percentage(%)'])

# 🎨 Highlighting
def highlight_rows(row):
    return ['background-color: #F5BA2E; color: black'] * len(row)

styled_df = (
    summary_df.style
    .apply(highlight_rows, axis=1)
    .format({'Percentage(%)': '{:.2f}'})
)

# 📊 Display summary
st.markdown("### 📈 Folder Movement Metrics Summary")
st.dataframe(styled_df)
