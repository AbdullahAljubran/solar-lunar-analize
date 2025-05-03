import streamlit as st
import geopandas as gpd
import pandas as pd
from solar_analysis import load_solar_data
from lunar_analysis import load_lunar_data  # ✅ استيراد ملف القمر

st.set_page_config(page_title="Eclipse Explorer", layout="wide")

st.title("🌘 Eclipse Explorer Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# ✅ فلتر لاختيار نوع الكسوف
eclipse_type = st.sidebar.radio("Choose Eclipse Type", ["Solar", "Lunar"])

# ✅ تحميل البيانات بناءً على الاختيار
@st.cache_data
def load_data(eclipse_type):
    if eclipse_type == "Solar":
        return load_solar_data()
    else:
        return load_lunar_data()

df = load_data(eclipse_type)

# ✅ الفلاتر المشتركة
era = st.sidebar.selectbox("Select Era", ["CE", "BCE"])
year = st.sidebar.number_input("Select Year", min_value=-3000, max_value=3000, value=2000, step=1)

# ✅ تصفية البيانات
is_ce = era.upper() == 'CE'
filtered_df = df[df['Year'].notna() & (df['Is_CE'] == is_ce) & (df['Year'] == year)]

# ✅ عرض النتائج
if filtered_df.empty:
    st.warning(f"No {eclipse_type.lower()} eclipse events found for year {year} {era}.")
else:
    st.success(f"{len(filtered_df)} {eclipse_type.lower()} eclipse events found for year {year} {era}.")

    # ✅ عرض الخريطة إن كانت إحداثيات موجودة
    #if 'Latitude' in filtered_df.columns and 'Longitude' in filtered_df.columns:
    st.map(filtered_df)

    # ✅ عرض الجدول حسب نوع الكسوف
    st.subheader("📄 Eclipse Data Table")
    if eclipse_type == "Solar":
        st.dataframe(filtered_df[[
            "Calendar-Date", "Eclipse-Type", "Eclipse-Magnitude", "Central-Duration",
            "Path-Width(km)", "Latitude", "Longitude", "Gamma"
        ]])
    else:  # Lunar
        st.dataframe(filtered_df[[
            "Calendar-Date", "Eclipse-Type", "Latitude", "Longitude", "Gamma",
            "Umbral-Magnitude", "Penumbral-Magnitude"
        ]])


    # ✅ رسومات بيانية أساسية
    # ✅ الرسوم البيانية والتحليلات حسب نوع الكسوف

if eclipse_type == "Solar":
    # توزيع نوع الكسوف
    st.subheader("📊 Eclipse Type Distribution")
    eclipse_type_counts = filtered_df['Eclipse-Type'].value_counts()
    st.bar_chart(eclipse_type_counts)

    # توزيع الحجم
    st.subheader("☀️ Eclipse Magnitude Distribution")
    st.line_chart(filtered_df[['Eclipse-Magnitude']].astype(float))

    # توزيع قيمة Gamma
    st.subheader("🌐 Gamma Value Distribution")
    gamma_values = pd.to_numeric(filtered_df['Gamma'], errors='coerce').dropna()
    if not gamma_values.empty:
        st.line_chart(gamma_values)
    else:
        st.info("No valid Gamma data available.")

    # توزيع عرض المسار
    st.subheader("📍 Path Width Distribution (if available)")
    valid_widths = pd.to_numeric(filtered_df['Path-Width(km)'], errors='coerce').dropna()
    if not valid_widths.empty:
        st.area_chart(valid_widths)
    else:
        st.info("No valid path width data available.")

elif eclipse_type == "Lunar":
    # توزيع نوع الكسوف
    st.subheader("📊 Eclipse Type Distribution")
    eclipse_type_counts = filtered_df['Eclipse-Type'].value_counts()
    st.bar_chart(eclipse_type_counts)

    # توزيع Umbral Magnitude
    st.subheader("🌑 Umbral Magnitude Distribution")
    umbral_magnitude = pd.to_numeric(filtered_df['Umbral-Magnitude'], errors='coerce').dropna()
    if not umbral_magnitude.empty:
        st.line_chart(umbral_magnitude)
    else:
        st.info("No valid Umbral Magnitude data available.")

    # توزيع Penumbral Magnitude
    st.subheader("🌘 Penumbral Magnitude Distribution")
    penumbral_magnitude = pd.to_numeric(filtered_df['Penumbral-Magnitude'], errors='coerce').dropna()
    if not penumbral_magnitude.empty:
        st.area_chart(penumbral_magnitude)
    else:
        st.info("No valid Penumbral Magnitude data available.")

    # توزيع Gamma
    st.subheader("🌐 Gamma Value Distribution")
    gamma_values = pd.to_numeric(filtered_df['Gamma'], errors='coerce').dropna()
    if not gamma_values.empty:
        st.line_chart(gamma_values)
    else:
        st.info("No valid Gamma data available.")


