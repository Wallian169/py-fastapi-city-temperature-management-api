from fastapi import FastAPI
from cities.router import router as cities_router

import cities

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(cities_router)
