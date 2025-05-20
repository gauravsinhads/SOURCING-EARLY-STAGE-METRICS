import streamlit as st
import pandas as pd
import plotly.express as px
import re
import numpy as np

# Set page config
st.set_page_config(page_title="iQor Talkpush Dashboard", layout="wide" )

# Custom CSS for button styling
st.markdown("""
<style>
    /* Button container styling */
    .sidebar .sidebar-content .block-container {
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
    }
    
    /* Button styling */
    div.stButton > button {
        width: 80%;
        border-radius: 4px 4px 0 0;
        border: 1px solid #e0e0e0;
        background-color: #E53855;
        color: white;
        text-align: left;
        padding: 8px 12px;
        margin: 0;
    }
    
    /* Selected button styling */
    div.stButton > button:focus {
        background-color: #2F76B9;
        border-bottom: 2px solid #F5F5F5;
        font-weight: bold;
    }
    
    /* Hover effect */
    div.stButton > button:hover {
        background-color: #e9ecef;
    }
</style>
""", unsafe_allow_html=True)



# Sidebar navigation buttons
st.sidebar.title("Pages")

def set_page(page_name):
    st.session_state.page = page_name

pages = ["SOURCING & EARLY STAGE METRICS" ]

for page in pages:
    st.sidebar.button(
        page,
        on_click=set_page,
        args=(page,),
        key=page
    )
#PAGE HOME_____________________________________________________________________________________________    
# Page content
if st.session_state.page == "SOURCING & EARLY STAGE METRICS":
    st.title("SOURCING & EARLY STAGE METRICS")


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
    
