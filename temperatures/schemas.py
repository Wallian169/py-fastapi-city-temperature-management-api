from datetime import datetime

import pydantic


class Temperature(pydantic.BaseModel):
    city_id: int
    date_time: datetime
    temperature: float
