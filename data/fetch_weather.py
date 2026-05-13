import requests
import pandas as pd

# Open-Meteo free historical weather API — no account or key needed
url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 48.85,          # Paris — change to your city's coordinates
    "longitude": 2.35,          # Find coords at maps.google.com → right click
    "start_date": "2023-01-01", # One full year
    "end_date": "2023-12-31",
    "hourly": "temperature_2m", # Hourly air temperature at 2m height
    "timezone": "Europe/Paris"  # Change to your timezone
}

print("Downloading weather data from Open-Meteo...")
response = requests.get(url, params=params)

# Check it worked
if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    exit()

data = response.json()

# Build a DataFrame with two columns: time and outdoor_T
df = pd.DataFrame({
    "time": data["hourly"]["time"],
    "outdoor_T": data["hourly"]["temperature_2m"]
})

# Convert time strings to proper datetime objects
df["time"] = pd.to_datetime(df["time"])

# Save to CSV
df.to_csv("data/weather.csv", index=False)

print(f"Done! Saved {len(df)} rows to data/weather.csv")
print(f"Temperature range: {df['outdoor_T'].min():.1f}°C to {df['outdoor_T'].max():.1f}°C")
print(df.head())  # Preview first 5 rows