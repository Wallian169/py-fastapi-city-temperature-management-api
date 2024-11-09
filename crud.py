from sqlalchemy.orm import Session

import models
import schemas


def get_all_cities(db: Session):
    return db.query(models.DBCity).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city_by_id(db: Session, city_id: int):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()
    if db_city:
        return db_city
    return None


def update_city_info(db: Session, city_id: int, city_info: schemas.CityUpdate):
    db_city = get_city_by_id(db, city_id)
    if db_city:
        db_city.additional_info = city_info.additional_info
        db.commit()
        db.refresh(db_city)
        return db_city

    return None


def delete_city_from_db(db: Session, city_id: int):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
        return db_city

    return None
