import streamlit as st
import pandas as pd
import plotly.express as px
import re
import numpy as np


    # Load the data
    df = pd.read_csv("SOURCING & EARLY STAGE METRICS.csv", parse_dates=['INVITATIONDT'])
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range filter
    min_date = df['INVITATIONDT'].min()
    max_date = df['INVITATIONDT'].max()
    start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    # Campaign filter
    campaigns = df['CAMPAIGNTITLE'].dropna().unique()
    selected_campaigns = st.sidebar.multiselect("Select Campaign Title(s)", campaigns, default=campaigns)
    
    # Source filter
    sources = df['SOURCE'].dropna().unique()
    selected_sources = st.sidebar.multiselect("Select Source(s)", sources, default=sources)
    
    # Work Location filter
    locations = df['WORKLOCATION'].dropna().unique()
    selected_locations = st.sidebar.multiselect("Select Work Location(s)", locations, default=locations)
    
    # Filter the data
    filtered_df = df[
        (df['INVITATIONDT'] >= pd.to_datetime(start_date)) &
        (df['INVITATIONDT'] <= pd.to_datetime(end_date)) &
        (df['CAMPAIGNTITLE'].isin(selected_campaigns)) &
        (df['SOURCE'].isin(selected_sources)) &
        (df['WORKLOCATION'].isin(selected_locations))
    ]
    
    # Apply the logic for 'Application to Unresponsive Folder'
    unresponsive_df = filtered_df[
        (filtered_df['FOLDER_FROM_TITLE'].isna() | (filtered_df['FOLDER_FROM_TITLE'] == "")) &
        (filtered_df['FOLDER_TO_TITLE'].str.contains("Unresponsive", na=False, case=False))
    ]
    
    # Count unique CAMPAIGNINVITATIONID
    count_unique_ids = unresponsive_df['CAMPAIGNINVITATIONID'].nunique()
    
    # Display the result
    st.subheader("Application to Unresponsive Folder")
    st.metric(label="Count of Unique Applications", value=count_unique_ids)
    
