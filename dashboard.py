import requests
import streamlit as st
import matplotlib.pyplot as plt
import datetime
import os

# API Key for AQI Data
API_KEY = "Add a key"

# List of cities
cities = ["Bangalore", "Delhi", "Mumbai", "Chennai", "Kolkata", "Hyderabad"]

# Streamlit Dashboard UI
st.title("🌍 Environmental Monitoring Dashboard")
st.subheader("Real-Time Air Quality and Pollution Monitoring")

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

    # Define AQI Levels
    if aqi <= 50:
        st.success("🟢 Good Air Quality")
        eco_tips = [
            "Maintain green spaces 🌱",
            "Reduce waste and recycle ♻️",
            "Use bicycles or walk 🚶‍♂️"
        ]
    elif aqi <= 100:
        st.info("🟡 Moderate Air Quality")
        eco_tips = [
            "Carpool to reduce emissions 🚗",
            "Avoid burning waste 🔥",
            "Plant more trees 🌳"
        ]
    elif aqi <= 150:
        st.warning("🟠 Unhealthy for Sensitive Groups")
        eco_tips = [
            "Limit outdoor activities 🏃",
            "Use air purifiers at home 🏠",
            "Advocate for pollution control 🏛️"
        ]
    else:
        st.error("🔴 Unhealthy Air Quality")
        eco_tips = [
            "Stay indoors when possible 🏠",
            "Wear a mask outdoors 😷",
            "Encourage public policy changes 📢"
        ]

    # Display Eco-Friendly Tips
    st.subheader("🌿 Eco-Friendly Actions You Can Take")
    for tip in eco_tips:
        st.write(f"- {tip}")

    # Simulated past AQI data (since free API doesn't provide historical data)
    timestamps = [(datetime.datetime.now() - datetime.timedelta(hours=i)).strftime("%H:%M") for i in range(10)][::-1]
    past_aqi = [aqi - i * 3 for i in range(10)]  # Fake trend for demo

    # Plot the AQI trend
    fig, ax = plt.subplots()
    ax.plot(timestamps, past_aqi, marker="o", linestyle="-", color="blue")
    ax.set_xlabel("Time")
    ax.set_ylabel("AQI Value")
    ax.set_title("AQI Trend Over Time")
    ax.grid(True)

    # Show the graph
    st.pyplot(fig)

else:
    st.error("❌ Failed to fetch AQI data. Check API Key or City Name.")

# Display Weather Data
if "current_weather" in weather_data:
    temperature = weather_data["current_weather"].get("temperature", "N/A")
    st.metric(label="🌡️ Temperature (°C)", value=temperature)
else:
    st.error("❌ Failed to fetch weather data.")

# ------------------------------------------
# 🌍 Crowd-Sourced Pollution Reporting System
# ------------------------------------------

st.subheader("📸 Report a Pollution Incident")

# User input fields
report_description = st.text_area("Describe the pollution issue (e.g., smoke, waste dumping, etc.)")
report_image = st.file_uploader("Upload an image (optional)", type=["jpg", "png", "jpeg"])

# Submit button
if st.button("Submit Report"):
    if report_description:
        report_data = f"**Pollution Report:** {report_description}\n"
        if report_image:
            report_image_path = f"reports/{report_image.name}"
            with open(report_image_path, "wb") as f:
                f.write(report_image.getbuffer())
            report_data += f"![Uploaded Image](reports/{report_image.name})"

        # Save report to file
        os.makedirs("reports", exist_ok=True)
        with open("reports/pollution_reports.txt", "a") as report_file:
            report_file.write(report_data + "\n\n")

        st.success("✅ Pollution report submitted successfully!")
    else:
        st.warning("⚠️ Please provide a description before submitting.")

# Show previous reports
if os.path.exists("reports/pollution_reports.txt"):
    st.subheader("📜 Recent Pollution Reports")
    with open("reports/pollution_reports.txt", "r") as report_file:
        reports = report_file.read()
        st.markdown(reports)
