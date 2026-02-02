from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging
import time

from services.weather_service import WeatherService

app = FastAPI()
templates = Jinja2Templates(directory="templates")
service = WeatherService()
# подключаем статику
app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather_app")

@app.middleware("http")
async def log_request(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = ((time.time() - start)*1000, 2)
    logger.info(f"{request.method} {request.url.path} completed in {duration} ms")
    return response

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("weather.html", {"request": request, "data": []})

@app.get("/weather", response_class=HTMLResponse)
async def weather_single(request: Request, city: str):
    result = await service.get_weather_for_city(city)
    return templates.TemplateResponse("weather.html", {"request": request, "data": [result]})

@app.get("/weather/all", response_class=HTMLResponse)
async def weather_all(request: Request):
    cities = ["Moscow", "Taipei", "Berlin", "London", "Warsaw", "New York", "Minsk"]
    results = await service.get_weather_for_cities(cities)
    return templates.TemplateResponse("weather.html", {"request": request, "data": results})
