import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import datetime
import numpy as np

st.set_page_config(page_title='Marmara Denizi Av Radarı', layout='wide')

st.title('🌊 Marmara Denizi Av Radarı')
st.markdown('Bu uygulama Marmara Denizi rüzgar, dalga ve klorofil verilerini analiz eder.')

# Sidebar Konfigürasyon
st.sidebar.header('Analiz Ayarları')
lat = st.sidebar.number_input('Enlem', value=40.65)
lon = st.sidebar.number_input('Boylam', value=28.30)

# Veri Çekme Fonksiyonu (Örnek)
@st.cache_data
def get_weather_data(lat, lon):
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'windspeed_10m,winddirection_10m,surface_pressure',
        'windspeed_unit': 'kmh',
        'forecast_days': 3
    }
    r = requests.get(url, params=params)
    if r.ok:
        data = r.json()
        df = pd.DataFrame(data['hourly'])
        df['time'] = pd.to_datetime(df['time'])
        return df
    return pd.DataFrame()

# Ana Ekran
df = get_weather_data(lat, lon)

if not df.empty:
    st.subheader('🌬️ Rüzgar Hızı Tahmini')
    fig = px.line(df, x='time', y='windspeed_10m', title='72 Saatlik Rüzgar Hızı (km/h)')
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader('📊 Ham Veri')
    st.dataframe(df.head())
else:
    st.error('Hava durumu verisi alınamadı.')

print('✅ app.py başarıyla güncellendi')
