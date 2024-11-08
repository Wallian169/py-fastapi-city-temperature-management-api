from typing import Optional

import pydantic


class CityBase(pydantic.BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    id: int

    class Config:
        orm_mode = True
