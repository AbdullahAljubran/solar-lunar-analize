import pandas as pd
import streamlit as st
import plotly.express as px
from astropy.time import Time 
#from astropy.coordinates import get_moon
from astropy.coordinates import get_body
from astropy.time import Time

time = Time.now()  # الوقت الحالي أو أي وقت تريده
moon = get_body('moon', time)  # احصل على موقع القمر

from sklearn.ensemble import RandomForestClassifier
from solar_analysis import load_solar_data  # This is our cleaned version

st.set_page_config(layout="wide")

st.title("🌞 Solar Eclipse Explorer")

# Load cleaned and processed data
df = load_solar_data()

# 🌍 A. Eclipse Path Map
fig_map = px.scatter_geo(
    df,
    lat='lat',
    lon='lon',
    color='Eclipse-Type',
    hover_name='Calendar-Date',
    projection='natural earth',
    title='Solar Eclipse Paths (2000 BCE - 3000 CE)'
)
st.plotly_chart(fig_map, use_container_width=True)

# 📊 B. Saros Cycle Analysis
fig_saros = px.line(
    df.groupby('Saros-Number').agg({'Eclipse-Magnitude': 'mean'}).reset_index(),
    x='Saros-Number',
    y='Eclipse-Magnitude',
    title='Average Eclipse Magnitude by Saros Cycle'
)
st.plotly_chart(fig_saros)

# ⏳ C. Century Timeline
century = df['Calendar-Date-Parsed'].dropna().dt.year // 100 * 100
df['Century'] = century
fig_timeline = px.histogram(
    df,
    x='Century',
    color='Eclipse-Type',
    barmode='stack',
    title='Eclipse Frequency by Century'
)
st.plotly_chart(fig_timeline)

# 🌙 D. Moon Phase
st.subheader("Moon Phase on Eclipse Date")
date = st.date_input('Select eclipse date')
moon_phase = get_moon(Time(str(date))).phase
st.metric("Moon Phase", f"{moon_phase:.0%} illuminated")

# 🤖 E. Eclipse Type Predictor
st.subheader("Eclipse Type Predictor (by Location)")
model = RandomForestClassifier()
model.fit(df[['lat', 'lon']], df['Eclipse-Type'])
user_lat = st.number_input('Latitude')
user_lon = st.number_input('Longitude')
if user_lat and user_lon:
    prediction = model.predict([[user_lat, user_lon]])[0]
    st.write(f"Predicted eclipse type: **{prediction}**")

# 🌌 Styling
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: url('https://www.nasa.gov/wp-content/uploads/2023/09/solar-eclipse-2017.jpg');
    background-size: cover;
    background-attachment: fixed;
}
.st-bw { background-color: rgba(0,0,0,0.7) !important; }
</style>
""", unsafe_allow_html=True)
