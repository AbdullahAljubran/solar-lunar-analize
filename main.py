import streamlit as st
import geopandas as gpd
from solar_analysis import load_solar_data
import pandas as pd

st.set_page_config(page_title="Solar Eclipse Explorer", layout="wide")

st.title("🌘 Solar Eclipse Explorer Dashboard")

# Load and cache data
@st.cache_data
def load_data():
    return load_solar_data()

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

era = st.sidebar.selectbox("Select Era", ["CE", "BCE"])
year = st.sidebar.number_input("Select Year", min_value=-3000, max_value=3000, value=2000, step=1)

# Apply filters
is_ce = era.upper() == 'CE'
filtered_df = df[df['Year'].notna() & (df['Is_CE'] == is_ce) & (df['Year'] == year)]

# Display results
if filtered_df.empty:
    st.warning(f"No eclipse events found for year {year} {era}.")
else:
    st.success(f"{len(filtered_df)} eclipse events found for year {year} {era}.")

    # Display map
    st.map(filtered_df)

    # Show eclipse data table
    st.dataframe(filtered_df[[
        "Calendar-Date", "Eclipse-Type", "Eclipse-Magnitude", "Central-Duration",
        "Path-Width(km)", "Latitude", "Longitude", "Gamma"
    ]])

    # Additional visualizations
    st.subheader("📊 Eclipse Type Distribution")
    eclipse_type_counts = filtered_df['Eclipse-Type'].value_counts()
    st.bar_chart(eclipse_type_counts)

    st.subheader("☀️ Eclipse Magnitude Distribution")
    st.line_chart(filtered_df[['Eclipse-Magnitude']].astype(float))
    
    # 🌐 Gamma value distribution
    st.subheader("🌐 Gamma Value Distribution")
    gamma_values = pd.to_numeric(filtered_df['Gamma'], errors='coerce').dropna()
    if not gamma_values.empty:
        st.line_chart(gamma_values)
    else:
        st.info("No valid Gamma data available.")

    st.subheader("📍 Path Width Distribution (if available)")
    valid_widths = pd.to_numeric(filtered_df['Path-Width(km)'], errors='coerce').dropna()
    if not valid_widths.empty:
        st.area_chart(valid_widths)
    else:
        st.info("No valid path width data available.")
        
        
    