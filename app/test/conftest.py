import pytest
from passlib.context import CryptContext
from app.db.connection import Session
from app.db.models import User as UserModel
from app.db.models import Asset as AssetModel
from app.db.models import Measurement as MeasurementModel


crypt_context = CryptContext(schemes=['sha256_crypt'])

@pytest.fixture()
def db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

@pytest.fixture()
def asset_on_db(db_session):
    Assets = [
        AssetModel( name='WTG 01'),
        AssetModel( name='WTG 02'),
        AssetModel( name='WTG 03'),
        AssetModel( name='WTG 04'),
    ]

    for Asset in Assets:
        db_session.add(Asset)
    db_session.commit()

    for Asset in Assets:
        db_session.refresh(Asset)
    
    yield Assets

    for Asset in Assets:
        db_session.delete(Asset)
    db_session.commit()


@pytest.fixture()
def measurements_on_db(db_session):
    asset = AssetModel(id=101 ,name='WTG 01')
    asset2 = AssetModel(id=102 ,name='WTG 02')
    

    db_session.add(asset)
    db_session.add(asset2)
    db_session.commit()
    db_session.refresh(asset)
    db_session.refresh(asset2)

    products = [
        MeasurementModel(timestamp= '2035-08-01 00:00:00.000 -0300', wind_speed= '13.032743', power= '2161.2974', air_temperature= '23.85818', assets_id=asset.id),
        MeasurementModel(timestamp= '2035-08-01 00:40:00.000 -0300', wind_speed= '12.891412', power= '2213.3948', air_temperature= '24.154732', assets_id=asset2.id),
        MeasurementModel(timestamp= '2035-08-01 01:20:00.000 -0300', wind_speed= '13.221848', power= '2204.2239', air_temperature= '22.701305', assets_id=asset2.id),
        MeasurementModel(timestamp= '2035-08-01 01:40:00.000 -0300', wind_speed= '13.2106085', power= '2224.8804', air_temperature= '22.256563', assets_id=asset.id),
    ]

    for product in products:
        db_session.add(product)
    db_session.commit()

    for product in products:
        db_session.refresh(product)
    
    yield products

    for product in products:
        db_session.delete(product)

    db_session.delete(asset)
    db_session.delete(asset2)
    db_session.commit()


@pytest.fixture()
def user_on_db(db_session):
    user = UserModel(
        username='Russell',
        password=crypt_context.hash('pass#')
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    yield user

    db_session.delete(user)
    db_session.commit()