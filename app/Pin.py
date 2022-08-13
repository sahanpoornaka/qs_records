from typing import Union

from pydantic import BaseModel


class Pin(BaseModel):
    pin_id: str
    width: float
    height: float
    breadth: float = 1.0
    times: int = 1
    x_coord: float
    y_coord: float
    remarks: str = ""
