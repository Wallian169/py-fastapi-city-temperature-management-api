from fastapi import FastAPI, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from cities import crud, schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    with SessionLocal() as db:
        yield db


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/cities/", response_model=list[schemas.City])
def get_cities(db=Depends(get_db)):
    return crud.get_all_cities(db)


@app.get("/cities/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db=Depends(get_db)):
    city = crud.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db=Depends(get_db)):
    return crud.create_city(db=db, city=city)


@app.patch("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city_info: schemas.CityUpdate, db=Depends(get_db)):
    city = crud.update_city_info(db, city_id, city_info)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db=Depends(get_db)):
    deleted_city = crud.delete_city_from_db(db=db, city_id=city_id)
    if not deleted_city:
        raise HTTPException(status_code=404, detail="City not found")

    return {"message": f"City was deleted"}
