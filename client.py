from aiohttp import ClientSession

class OpenMeteoClient:
    GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self):
        self.session = None
        self.cache = {} #city->(lat, lon)

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


    async def get_coordinates(self, city):
        city_key = city.lower()

        # Кэширование
        if city in self.cache:
            return self.cache[city_key]

        params = {"name": city, "limit": "1"}
        async with self.session.get(self.GEO_URL, params=params) as resp:
            data = await resp.json()

        if "results" in data and data["results"]:
            r = data["results"][0]
            lat, lon = r["latitude"], r["longitude"]
            self.cache[city_key] = (lat, lon)
            return lat, lon

        return None, None

    async def get_current_weather(self, city: str):
        lat, lon = await self.get_coordinates(city)
        if lat is None or lon is None:
            return None

        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        }

        async with self.session.get(self.WEATHER_URL, params=params) as resp:
            data = await resp.json()

        if "current_weather" not in data:
            return None

        w = data["current_weather"]

        return {
            "city": city,
            "temperature": w["temperature"],
            "windspeed": w["windspeed"],
            "winddirection": w["winddirection"],
            "time": w["time"]
        }

        async with self.session.get(self.WEATHER_URL, params=params) as resp:
            data = await resp.json()

        if "current_weather" not in data:
            return f"{city}: No weather data"
        temp = data["current_weather"]["temperature"]
        return f"{city}: {temp}°C"