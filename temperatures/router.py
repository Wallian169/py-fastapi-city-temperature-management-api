from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from depencies import get_db
from temperatures import crud
from temperatures import schemas

router = APIRouter()

@router.post("/temperatures/")
def update_temperatures(db: Session = Depends(get_db)):
    message = crud.create_temperatures_record(db)
    return {"message": message}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def get_temperatures(db: Session = Depends(get_db)):
    return crud.get_temperatures_records(db)
