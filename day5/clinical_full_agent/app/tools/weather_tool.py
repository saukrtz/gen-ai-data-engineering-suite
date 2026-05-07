import requests

def get_weather(city: str = "New York"):
    """
    Fetches real-time weather data for a city using Open-Meteo API.
    Note: In a real app, you'd geocode the city name to lat/long. 
    For this demo, we'll use a fixed location (Bangalore) for speed.
    """
    url = "https://api.open-meteo.com/v1/forecast?latitude=12.9716&longitude=77.5946&current_weather=True"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data["current_weather"]["temperature"]
            wind = data["current_weather"]["windspeed"]
            return {
                "city": city,
                "temperature": f"{temp}°C",
                "windspeed": f"{wind} km/h",
                "condition": "Fetched from Open-Meteo"
            }
        return {"error": "Weather API unreachable"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(get_weather())
