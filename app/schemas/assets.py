from app.schemas.base import CustomBaseModel


class Asset(CustomBaseModel):
    id: int
    name: str
    

class AssetOutput(Asset):
    id: int

    class Config:
        orm_mode=True