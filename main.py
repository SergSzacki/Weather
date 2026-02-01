from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import asyncio
from client import OpenMeteoClient
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-app")




app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)

    logger.info(f"{request.method} {request.url.path} completed in {duration} ms")
    return response
@app.get('/', response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>Weather App</title>
        </head>
        <body>
            <h1>Weather Checker</h1>
            
            <form action="/weather" method="get">
                <label>Enter city:</label>
                <input type="text" name="city" required>
                <button type="submit">Check</button>
            </form>
            
            <p>Or check multiple cities</p>
            <a href="/weather/all">Show all</a>
        </body>
    </html>
    """
@app.get('/weather', response_class=HTMLResponse)
async def weather_single(city: str):
    async with OpenMeteoClient() as api:
        result = await api.get_current_weather(city)

    return f"""
    <html>
        <body>
            <h2>Weather for {city}</h2>
            <p>{result}</p>
            <a href="/">Back</a>
        </body>
    </html>
    """

@app.get('/weather/all', response_class=HTMLResponse)
async def weather_all():
    cities = ['Moscow', 'Paris', 'Tokyo', 'London', 'New York', 'Warsaw', 'Minsk']
    async with OpenMeteoClient() as api:
        tasks =[api.get_current_weather(c) for c in cities]
        result = await asyncio.gather(*tasks)
        rows = "".join(f"<tr><td>{r}</td></tr>" for r in result)

        return f"""
        <html>
            <body>
                <h2>Weather for multiple cities</h2>
                <table border="1" cellpadding="5">
                    {rows}
                </table>
                <a href="/">Back</a>
            </body>
        </html>
        """
