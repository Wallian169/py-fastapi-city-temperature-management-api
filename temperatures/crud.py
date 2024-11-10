import os
from datetime import datetime
from typing import Callable

import requests

from sqlalchemy.orm import Session
from dotenv import load_dotenv

from cities.crud import get_all_cities
from temperatures import models

load_dotenv("../.env")

API_URL = "http://api.weatherapi.com/v1/current.json"
KEY = os.getenv("API_KEY")


def get_temperature_from_api(name: str) -> float | None:
    params = {
        "key": "47a3629b3beb44a48dc134140241409",
        "q": name
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        return data["current"]["temp_c"]
    else:
        print(data.get("error", {}).get("message", "Unknown error"))
        return None

def timer(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        end = datetime.now()
        elapsed_time = (end - start).total_seconds()
        print(f"Time elapsed: {elapsed_time:.6f} seconds")
    return inner

@timer
def create_temperatures_record(db: Session):
    cities = get_all_cities(db)
    counter = 0

    for city in cities:
        temperature = get_temperature_from_api(city.name)
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
