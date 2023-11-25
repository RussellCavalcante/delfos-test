from sqlalchemy.orm import Session
from app.db.models import Asset as AssetModel
from app.schemas.assets import Asset, AssetOutput
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import File
import pandas as pd
import json


class AssetUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def add_Asset(self, Asset: Asset):
        Asset_model = AssetModel(**Asset.dict())
        self.db_session.add(Asset_model)
        self.db_session.commit()

    def list_assets(self, page: int = 1, size: int = 50):
        assets_on_db = self.db_session.query(AssetModel)
        params = Params(page=page, size=size)
        return paginate(assets_on_db, params=params)
    
    def add_file_assets(self, file:File):
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser um CSV")
        try:
            df = pd.read_csv(file.file, delimiter=',', header=None)
            json_list = []
            for index, row in df.iterrows():
                if row[0] == 'asset_id':
                    continue
                data_dict = {
                    'id': row[0],
                    'name': row[1],
                }
                json_data = json.dumps(data_dict)
                json_list.append(json_data)
            
            for json_data in json_list:
                json_object = json.loads(json_data)

                Asset_model = AssetModel(**json_object)
                self.db_session.add(Asset_model)
                self.db_session.commit()
        
        except pd.errors.EmptyDataError:
            raise HTTPException(status_code=400, detail="Arquivo CSV vazio ou nao possui asset")


    def delete_Asset(self, id: int):
        Asset_model = self.db_session.query(AssetModel).filter_by(id=id).first()
        if not Asset_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Asset not found')
        
        self.db_session.delete(Asset_model)
        self.db_session.commit()

    def serialize_Asset(self, Asset_model: AssetModel):
        return AssetOutput(**Asset_model.__dict__)
