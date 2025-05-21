import streamlit as st
import pandas as pd

# Set page title
st.set_page_config(page_title="SOURCING & EARLY STAGE METRICS")

# Load the data
df = pd.read_csv("SOURCING & EARLY STAGE METRICS.csv")

# Convert date columns to datetime
df['INVITATIONDT'] = pd.to_datetime(df['INVITATIONDT'], errors='coerce')
df['ACTIVITY_CREATED_AT'] = pd.to_datetime(df['ACTIVITY_CREATED_AT'], errors='coerce')
df['INSERTEDDATE'] = pd.to_datetime(df['INSERTEDDATE'], errors='coerce')

# Custom colors for styling
custom_colors = ["#2F76B9", "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00", "#B4BBBE", "#e6657b", "#026df5", "#5aede2"]

# Set the main title
st.title("SOURCING & EARLY STAGE METRICS")

# Filters
st.subheader("Filters")

min_date = df['INVITATIONDT'].min()
max_date = df['INVITATIONDT'].max()

start_date, end_date = st.date_input("Select Date Range", [min_date, max_date])

with st.expander("Select Work Location(s)"):
    selected_worklocations = st.multiselect(
        "Work Location",
        options=sorted(df['WORKLOCATION'].dropna().unique()),
        default=None
    )

with st.expander("Select Campaign Title(s)"):
    selected_campaigns = st.multiselect(
        "Campaign Title",
        options=sorted(df['CAMPAIGNTITLE'].dropna().unique()),
        default=None
    )

# Filter data based on selections
df_filtered = df[
    (df['INVITATIONDT'] >= pd.to_datetime(start_date)) &
    (df['INVITATIONDT'] <= pd.to_datetime(end_date))
]

if selected_worklocations:
    df_filtered = df_filtered[df_filtered['WORKLOCATION'].isin(selected_worklocations)]

if selected_campaigns:
    df_filtered = df_filtered[df_filtered['CAMPAIGNTITLE'].isin(selected_campaigns)]

# Drop rows without campaign ID
df_filtered = df_filtered.dropna(subset=['CAMPAIGNINVITATIONID'])

# Get total unique campaign invitation IDs for percentage calculation
total_unique_ids = df_filtered['CAMPAIGNINVITATIONID'].nunique()

# Function to calculate metrics
def compute_metric(title, from_condition, to_condition):
    filtered = df_filtered.copy()

    if from_condition == 'empty':
        mask = filtered['FOLDER_FROM_TITLE'].isna()
    else:
        mask = filtered['FOLDER_FROM_TITLE'].fillna('').str.strip().str.lower() == from_condition.lower()

    mask &= filtered['FOLDER_TO_TITLE'].fillna('').str.lower().str.contains(to_condition.lower())

    count = filtered[mask]['CAMPAIGNINVITATIONID'].nunique()
    percentage = round((count / total_unique_ids * 100), 2) if total_unique_ids else 0

    return {"Metric": title, "Count": count, "Percentage(%)": percentage}

# Calculate all required metrics
summary_data = [
    compute_metric("Application to Unresponsive Folder", 'empty', 'Unresponsive'),
    compute_metric("Unresponsive Folder to Passed MQ Folder", 'Unresponsive', 'Passed MQ'),
    compute_metric("Unresponsive Folder to Failed MQ Folder", 'Unresponsive', 'Failed MQ'),
    compute_metric("Unresponsive Folder to Cold Leads Folder", 'Unresponsive', 'Cold Leads'),
    compute_metric("Application to Unresponsive TS Folder", 'empty', 'Unresponsive Talkscore'),
    compute_metric("Unresponsive TS Folder to Passed MQ Folder", 'Unresponsive Talkscore', 'Passed MQ'),
    compute_metric("Unresponsive TS Folder to Failed MQ Folder", 'Unresponsive Talkscore', 'Failed MQ'),
    compute_metric("Unresponsive TS Folder to Cold Leads TS Folder", 'Unresponsive Talkscore', 'Cold Leads Talkscore'),
    compute_metric("Application to Unresponsive TS Retake Folder", 'empty', 'Unresponsive Talkscore Retake'),
    compute_metric("Unresponsive TS Retake Folder to Passed MQ Folder", 'Unresponsive Talkscore Retake', 'Passed MQ'),
    compute_metric("Unresponsive TS Retake Folder to Failed MQ Folder", 'Unresponsive Talkscore Retake', 'Failed MQ'),
    compute_metric("Unresponsive TS Retake Folder to Cold Lead TS Retake Folder", 'Unresponsive Talkscore Retake', 'Cold Leads Talkscore Retake')    
]

# Create a DataFrame
summary_df = pd.DataFrame(summary_data)

# Display summary table
st.markdown("### Folder Movement Summary")
st.dataframe(
    summary_df.style        
        .applymap(lambda _: 'color: black', subset=pd.IndexSlice[:, ['Count', 'Percentage(%)']])
)
