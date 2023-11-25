from app.schemas.base import CustomBaseModel
from app.schemas.assets import Asset


class Measurements(CustomBaseModel):
    timestamp : str
    wind_speed : str
    power : str
    air_temperature : str



class MeasurementsInput(CustomBaseModel):
    asset_id: int
    measurements: Measurements


class AvarageOutput(CustomBaseModel):
    avarage_value: float
    asset_id: int
    timestamp: str


class MeasurementsOutput(Measurements):
    id: int
    asset: Asset

    class Config:
        orm_mode=True