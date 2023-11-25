from sqlalchemy.orm import Session
from sqlalchemy import or_ , text
from fastapi.exceptions import HTTPException
from fastapi import status
from app.db.models import Measurement as MeasurementsModel
from app.db.models import Asset as AssetModel
from app.schemas.measurements import Measurements, MeasurementsOutput , AvarageOutput
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import File
import pandas as pd
import json


class MeasurementsUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_measurements(self, measurements: Measurements, asset_id: int):
        asset = self.db_session.query(AssetModel).filter_by(id=asset_id).first()
    
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No Asset was found with id {asset_id}')
        
        measurements_model = MeasurementsModel(**measurements.dict())
        measurements_model.assets_id = asset.id

        self.db_session.add(measurements_model)
        self.db_session.commit()

    def add_file_measurements(self, file:File):
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser um CSV")

        # Lê o conteúdo do arquivo CSV usando o Pandas
        try:

            df = pd.read_csv(file.file, delimiter=',', header=None)
            json_list = []
            # Itera sobre as linhas do DataFrame
            for index, row in df.iterrows():
                # Converte a linha para um dicionário
                if row[0] == 'asset_id':
                    continue
                
                data_dict = {
                    'assets_id': row[0],
                    'timestamp': row[1],
                    'wind_speed': row[2],
                    'power': row[3],
                    'air_temperature': row[4]
                }
                
                # Converte o dicionário em JSON e adiciona à lista
                json_data = json.dumps(data_dict)
                json_list.append(json_data)
            
            for json_data in json_list:
                json_object = json.loads(json_data)
                print(json_object)
                # Faça algo com o DataFrame, por exemplo, imprima as primeiras linhas

                asset = self.db_session.query(AssetModel).filter_by(id=json_object["assets_id"]).first()
                
                if not asset:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No Asset was found with id {json_object["assets_id"]}')
                

                measurements_model = MeasurementsModel(**json_object)
                

                self.db_session.add(measurements_model)
                self.db_session.commit()
        
        except pd.errors.EmptyDataError:
            raise HTTPException(status_code=400, detail="Arquivo CSV vazio ou nao possui asset")
  

    def update_measurements(self, id: int, measurements: Measurements):
        measurements_on_db = self.db_session.query(MeasurementsModel).filter_by(id=id).first()

        if measurements_on_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No Measurements was found with the given id')
        
        Measurements_on_db.timestamp = measurements.timestamp
        measurements_on_db.wind_speed = measurements.wind_speed
        measurements_on_db.power = measurements.power
        measurements_on_db.air_temperature = measurements.air_temperature

        self.db_session.add(measurements_on_db)
        self.db_session.commit()

    def delete_Measurements(self, id: int):
        Measurements_on_db = self.db_session.query(MeasurementsModel).filter_by(id=id).first()

        if Measurements_on_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No Measurements was found with the given id')
        
        self.db_session.delete(Measurements_on_db)
        self.db_session.commit()

    def list_Measurementss(self, page: int = 1, size: int = 50, search: str = ''):
        Measurements_on_db = self.db_session.query(MeasurementsModel).filter(
            or_(
                MeasurementsModel.timestamp.ilike(f'%{search}%'),
                MeasurementsModel.wind_speed.ilike(f'%{search}'),
                MeasurementsModel.power.ilike(f'%{search}%'),
                MeasurementsModel.air_temperature.ilike(f'%{search}')
            # or_(AssetModel.id.ilike(f'%{search}%'),
            #     AssetModel.name.ilike(f'%{search}%')
            # )
            )
        )

        
        params = Params(page=page, size=size)
        page = paginate(Measurements_on_db, params=params)

        return page

    
    def list_average_value_(self, specific_column: str = '', asset_id: int = 1, timestamp: str ='' ):
        # asset_id: int = 1, specific_column: str = '', timestamp: str =''

        sql_query = text(f"""SELECT a.name, AVG(CAST({specific_column} AS numeric)), m.assets_id, m.timestamp
                            FROM assets a 
                            LEFT JOIN measurements m ON a.id = m.assets_id 
                            WHERE assets_id = {asset_id} AND timestamp = '{timestamp}' GROUP BY a.name, m.assets_id, m.timestamp; """)
        # print(asset_id, specific_column, timestamp)
        query_on_db = self.db_session.execute(sql_query)
        data = query_on_db.fetchall()
        # print(data, sql_query)
        # input()
        chave = ['name','avarage_value', 'asset_id', 'timestamp']

        dicionario = dict(zip(chave, data[0]))

        avarage_output = self._serialize_avarage(dicionario)

        return avarage_output


    
    def _serialize_Measurements(self, Measurements_on_db: MeasurementsModel):
        Measurements_dict = Measurements_on_db.__dict__
        Measurements_dict['Asset'] = Measurements_on_db.Asset.__dict__

        return MeasurementsOutput(**Measurements_dict)
    
    def _serialize_avarage(self, avarageoutput: AvarageOutput):
        Avarage_dict = avarageoutput
        # print(Avarage_dict)
        
        # print(float(Avarage_dict['avarage_value']), type(float(Avarage_dict['avarage_value'])))
        
        Avarage_dict['avarage_value'] = float(Avarage_dict['avarage_value'])
        # print(Avarage_dict)
        # input()

        return AvarageOutput(**Avarage_dict)
