from fastapi import APIRouter, File, UploadFile,  Depends, Response, status, Query
from sqlalchemy.orm import Session
from app.schemas.assets import Asset, AssetOutput
from app.routes.deps import get_db_session, auth
from app.use_cases.assets import AssetUseCases
from fastapi_pagination import Page


router = APIRouter(prefix='/asset', tags=['Asset'], dependencies=[Depends(auth)])


@router.post('/add', status_code=status.HTTP_201_CREATED, description="Add new asset")
def add_Asset(
    Asset: Asset,
    db_session: Session = Depends(get_db_session)
):
    uc = AssetUseCases(db_session=db_session)
    uc.add_Asset(Asset=Asset)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post('/uploadfile', status_code=status.HTTP_201_CREATED, description='Add new Measurements')
def create_upload_file(
    file: UploadFile = File(...),
    db_session: Session = Depends(get_db_session)
):
    uc = AssetUseCases(db_session=db_session)
    uc.add_file_assets(
        file=file
    )

    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/list', response_model=Page[AssetOutput], description="List assets")
def list_categories(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Size of page"),
    db_session: Session = Depends(get_db_session)
):
    uc = AssetUseCases(db_session=db_session)
    response = uc.list_assets(page=page, size=size)

    return response


@router.delete('/delete/{id}', description="Delete asset")
def delete_Asset(
    id: int,
    db_sesion: Session = Depends(get_db_session)
):
    uc = AssetUseCases(db_session=db_sesion)
    uc.delete_Asset(id=id)

    return Response(status_code=status.HTTP_200_OK)
