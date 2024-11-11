import os
from datetime import datetime
from typing import Callable

import httpx

from sqlalchemy.orm import Session
from dotenv import load_dotenv

from cities.crud import get_all_cities
from temperatures import models

load_dotenv()

API_URL = "http://api.weatherapi.com/v1/current.json"
KEY = os.getenv("API_KEY")


async def get_temperature_from_api(name: str) -> float | None:
    params = {
        "key": KEY,
        "q": name
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data["current"]["temp_c"]

def timer(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        end = datetime.now()
        elapsed_time = (end - start).total_seconds()
        print(f"Time elapsed: {elapsed_time:.6f} seconds")
    return inner

@timer
async def create_temperatures_record(db: Session):
    cities = get_all_cities(db)
    counter = 0

    for city in cities:
        temperature = await get_temperature_from_api(city.name)
        if temperature:
            record = models.Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature,
            )
            db.add(record)
            counter += 1

    db.commit()

    return counter


def get_temperatures_records(db: Session):
    temperatures = db.query(models.Temperature).all()
    return temperatures
