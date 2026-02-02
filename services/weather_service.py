import asyncio
from client import OpenMeteoClient

class WeatherService:

    async def get_weather_for_city(self, city: str):
        async with OpenMeteoClient() as api:
            data = await api.get_current_weather(city)

        if not data:
            return {"city": city, "temperature": None, "windspeed": None, "winddirection": None, "time": None}

        return {
            "city": city,
            "temperature": data["temperature"],
            "windspeed": data["windspeed"],
            "winddirection": data["winddirection"],
            "time": data["time"]
        }

    async def get_weather_for_cities(self, cities: list[str]):
        async with OpenMeteoClient() as api:
            tasks = [api.get_current_weather(city) for city in cities]
            results = await asyncio.gather(*tasks)

        output = []
        for city, data in zip(cities, results):
            if not data:
                output.append(
                    {"city": city, "temperature": None, "windspeed": None, "winddirection": None, "time": None})
            else:
                output.append({
                    "city": city,
                    "temperature": data["temperature"],
                    "windspeed": data["windspeed"],
                    "winddirection": data["winddirection"],
                    "time": data["time"]
                })

        return output
