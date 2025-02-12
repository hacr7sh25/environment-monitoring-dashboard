import requests
import streamlit as st
import matplotlib.pyplot as plt
import datetime

# Streamlit command to run: streamlit run dashboard.py

# API Key for AQI Data
API_KEY = "9d7c2e651f004587d12a7809d2b6e43332eaa17d"

# List of cities
cities = ["Bangalore", "Delhi", "Mumbai", "Chennai", "Kolkata", "Hyderabad"]

# Streamlit Dashboard UI
st.title("🌍 Environmental Monitoring Dashboard")
st.subheader("Real-Time Air Quality and Weather Monitoring")

# Select city
CITY = st.selectbox("Select a city:", cities)

# AQI API URL
aqi_url = f"https://api.waqi.info/feed/{CITY}/?token={API_KEY}"
aqi_response = requests.get(aqi_url)
aqi_data = aqi_response.json()

# Weather API URL
weather_url = f"https://api.open-meteo.com/v1/forecast?latitude=12.97&longitude=77.59&current_weather=true"
weather_response = requests.get(weather_url)
weather_data = weather_response.json()

# Fetch and display AQI data
if aqi_data["status"] == "ok":
    aqi = aqi_data["data"]["aqi"]
    st.metric(label="🌫️ Air Quality Index (AQI)", value=aqi)

    # Define AQI Levels and Recommendations
    if aqi <= 50:
        st.success("🟢 Good Air Quality - Enjoy outdoor activities!")
    elif aqi <= 100:
        st.info("🟡 Moderate Air Quality - Safe for most, but be cautious if sensitive.")
    elif aqi <= 150:
        st.warning("🟠 Unhealthy for Sensitive Groups - Reduce outdoor activities if needed.")
    else:
        st.error("🔴 Unhealthy Air Quality - Avoid outdoor exertion and wear a mask.")

    # Simulated past AQI data
    timestamps = [(datetime.datetime.now() - datetime.timedelta(hours=i)).strftime("%H:%M") for i in range(10)][::-1]
    past_aqi = [aqi - i * 3 for i in range(10)]  # Fake trend for demo

    # Plot AQI trend
    fig, ax = plt.subplots()
    ax.plot(timestamps, past_aqi, marker="o", linestyle="-", color="blue")
    ax.set_xlabel("Time")
    ax.set_ylabel("AQI Value")
    ax.set_title("AQI Trend Over Time")
    ax.grid(True)

    # Show the graph
    st.pyplot(fig)

    # Pollution Source Analysis (Simulated Data)
    st.subheader("🔬 Pollution Source Analysis")
    pollution_sources = {
        "Vehicle Emissions": 40,
        "Industrial Waste": 25,
        "Construction Dust": 15,
        "Agricultural Burning": 10,
        "Other": 10
    }

    # Plot pollution source distribution
    fig2, ax2 = plt.subplots()
    ax2.pie(pollution_sources.values(), labels=pollution_sources.keys(), autopct="%1.1f%%", colors=["red", "orange", "yellow", "green", "blue"])
    ax2.set_title("Estimated Contribution of Pollution Sources")

    st.pyplot(fig2)

else:
    st.error("❌ Failed to fetch AQI data. Check API Key or City Name.")

# Display Weather Data
if "current_weather" in weather_data:
    temperature = weather_data["current_weather"].get("temperature", "N/A")
    weather_code = weather_data["current_weather"].get("weathercode", "N/A")

    # Map weather codes to icons
    weather_icons = {
        0: "☀️ Clear Sky",
        1: "🌤️ Partly Cloudy",
        2: "⛅ Cloudy",
        3: "☁️ Overcast",
        45: "🌫️ Foggy",
        48: "🌫️ Dense Fog",
        51: "🌦️ Light Drizzle",
        53: "🌧️ Moderate Drizzle",
        55: "🌧️ Heavy Drizzle",
        61: "🌦️ Light Rain",
        63: "🌧️ Moderate Rain",
        65: "🌧️ Heavy Rain",
        95: "⛈️ Thunderstorm",
        99: "🌪️ Extreme Storm"
    }

    weather_description = weather_icons.get(weather_code, "Unknown Weather")

    st.metric(label="🌡️ Temperature (°C)", value=temperature)
    st.write(f"Weather Condition: {weather_description}")

else:
    st.error("❌ Failed to fetch weather data.")
