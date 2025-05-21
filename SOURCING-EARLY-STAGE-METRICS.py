import streamlit as st
import pandas as pd

# Load the CSV file
df = pd.read_csv('SOURCING & EARLY STAGE METRICS.csv')

# Convert date columns to datetime
df['INVITATIONDT'] = pd.to_datetime(df['INVITATIONDT'], errors='coerce')
df['ACTIVITY_CREATED_AT'] = pd.to_datetime(df['ACTIVITY_CREATED_AT'], errors='coerce')
df['INSERTEDDATE'] = pd.to_datetime(df['INSERTEDDATE'], errors='coerce')

# Set custom colors
custom_colors = ["#2F76B9", "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00", "#B4BBBE", "#e6657b", "#026df5", "#5aede2"]

# Set the title
st.title("SOURCING & EARLY STAGE METRICS")

# Sidebar Filters
st.subheader("Filters")

min_date = df['INVITATIONDT'].min()
max_date = df['INVITATIONDT'].max()

start_date, end_date = st.date_input("Select Date Range", [min_date, max_date])

with st.expander("Select Work Location(s)"):
    selected_locations = st.multiselect("Work Location", options=sorted(df['WORKLOCATION'].dropna().unique()), default=None)

with st.expander("Select Campaign Title(s)"):
    selected_campaigns = st.multiselect("Campaign Title", options=sorted(df['CAMPAIGNTITLE'].dropna().unique()), default=None)

# Apply filters
df_filtered = df[
    (df['INVITATIONDT'] >= pd.to_datetime(start_date)) &
    (df['INVITATIONDT'] <= pd.to_datetime(end_date))
]

if selected_locations:
    df_filtered = df_filtered[df_filtered['WORKLOCATION'].isin(selected_locations)]

if selected_campaigns:
    df_filtered = df_filtered[df_filtered['CAMPAIGNTITLE'].isin(selected_campaigns)]

# Drop rows where campaign ID is missing
df_valid = df_filtered.dropna(subset=['CAMPAIGNINVITATIONID'])

# Calculate total unique campaign invitations
total_unique_ids = df_valid['CAMPAIGNINVITATIONID'].nunique()

# Define function to compute metric
def compute_metric_adjusted(title, from_title, to_title_contains, from_empty=False):
    if from_empty:
        condition = (
            df_valid['FOLDER_FROM_TITLE'].isna()
        ) & (
            df_valid['FOLDER_TO_TITLE'].fillna('').str.lower().str.contains(to_title_contains.lower())
        )
    else:
        condition = (
            df_valid['FOLDER_FROM_TITLE'].fillna('').str.strip().str.lower() == from_title.lower()
        ) & (
            df_valid['FOLDER_TO_TITLE'].fillna('').str.lower().str.contains(to_title_contains.lower())
        )
    count = df_valid[condition]['CAMPAIGNINVITATIONID'].nunique()
    percentage = round((count / total_unique_ids * 100), 2) if total_unique_ids else 0
    return {'Metric': title, 'Count': count, 'Percentage(%)': percentage}

# Compute all rows
metrics = [
    compute_metric_adjusted('Application to Unresponsive Folder', '', 'Unresponsive', from_empty=True),
    compute_metric_adjusted('Unresponsive Folder to Passed MQ Folder', 'Unresponsive', 'Passed MQ'),
    compute_metric_adjusted('Unresponsive Folder to Failed MQ Folder', 'Unresponsive', 'Failed MQ'),
    compute_metric_adjusted('Unresponsive Folder to Cold Leads Folder', 'Unresponsive', 'Cold Leads')
]

# Create summary DataFrame
summary_df = pd.DataFrame(metrics)

# Display the results
st.markdown("### Folder Transition Summary")
st.dataframe(summary_df.style
    .applymap(lambda _: f'background-color: {custom_colors[2]}; color: black', subset=pd.IndexSlice[["Application to Unresponsive Folder"], ['Metric']])
    .applymap(lambda _: 'color: black', subset=pd.IndexSlice[:, ['Count', 'Percentage(%)']])
)
