from typing import Optional

import pydantic


class City(pydantic.BaseModel):
    id: int
    name: str
    additional_info: Optional[str] = None
