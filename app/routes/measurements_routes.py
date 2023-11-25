from fastapi import APIRouter, File, UploadFile, Response, Depends, status, Query
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session, auth
from app.use_cases.measurements import MeasurementsUseCases
from app.schemas.measurements import Measurements, MeasurementsInput, MeasurementsOutput, AvarageOutput
from fastapi_pagination import Page


router = APIRouter(prefix='/measurement', tags=['Measurements'], dependencies=[Depends(auth)])


@router.post('/add', status_code=status.HTTP_201_CREATED, description='Add new Measurements')
def add_Measurements(
    Measurements_input: MeasurementsInput,
    db_session: Session = Depends(get_db_session)
):
    uc = MeasurementsUseCases(db_session=db_session)
    uc.add_measurements(
        measurements=Measurements_input.measurements,
        asset_id=Measurements_input.asset_id
    )

    return Response(status_code=status.HTTP_201_CREATED)

@router.post('/uploadfile', status_code=status.HTTP_201_CREATED, description='Add new Measurements')
def create_upload_file(
    file: UploadFile = File(...),
    db_session: Session = Depends(get_db_session)
):
    uc = MeasurementsUseCases(db_session=db_session)
    uc.add_file_measurements(
        file=file
    )

    return Response(status_code=status.HTTP_201_CREATED)


@router.put('/update/{id}', description='Update Measurements')
def update_Measurements(
    id: int,
    Measurements: Measurements,
    db_session: Session = Depends(get_db_session)
):
    uc = MeasurementsUseCases(db_session=db_session)
    uc.update_Measurements(id=id, Measurements=Measurements)

    return Response(status_code=status.HTTP_200_OK)


@router.delete('/delete/{id}', description='Delete Measurements')
def delete_Measurements(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    uc = MeasurementsUseCases(db_session=db_session)
    uc.delete_Measurements(id=id)

    return Response(status_code=status.HTTP_200_OK)


@router.get('/list', response_model=Page[MeasurementsOutput], description='List Measurementss')
def list_Measurements(
    search: str = '',
    page: int = Query(1, ge=1, description='Page number'),
    size: int = Query(50, ge=1, le=100, description='Page size'),
    db_session: Session = Depends(get_db_session)
):
    uc = MeasurementsUseCases(db_session=db_session)
    Measurementss = uc.list_Measurementss(page=page, size=size, search=search)

    return Measurementss

@router.get('/list_average_value', response_model=AvarageOutput, description='List Average Value')
def list_average_value(
    timestamp: str = '',
    specific_column: str = '',
    asset_id: int = Query(1, ge=1, description='Asset Number'),
    db_session: Session = Depends(get_db_session)
):
    uc = MeasurementsUseCases(db_session=db_session)
    average = uc.list_average_value_(specific_column=specific_column, asset_id=asset_id, timestamp=timestamp)

    return average
