import pytest
from fastapi.exceptions import HTTPException
from app.db.models import Measurement as MeasurementModel
from app.schemas.measurements import Measurements, MeasurementsOutput
from app.use_cases.measurements import MeasurementsUseCases
from fastapi_pagination import Page


def test_add_measurements_uc(db_session, asset_on_db):
    uc = MeasurementsUseCases(db_session)

    measurements = Measurements(
        timestamp= '2035-08-01 00:00:00.000 -0300',
        wind_speed= '13.032743',
        power= '2161.2974',
        air_temperature= '23.85818'
    )


    uc.add_measurements(measurements=measurements, asset_id=asset_on_db[0].id)

    measurements_on_db = db_session.query(MeasurementModel).first()

    assert measurements_on_db is not None
    assert measurements_on_db.timestamp == measurements.timestamp
    assert measurements_on_db.wind_speed == measurements.wind_speed
    assert measurements_on_db.power == measurements.power
    assert measurements_on_db.air_temperature == measurements.air_temperature
    assert measurements_on_db.assets_id == asset_on_db[0].id

    db_session.delete(measurements_on_db)
    db_session.commit()


def test_add_measurements_uc_invalid_asset(db_session):
    uc = MeasurementsUseCases(db_session)

    measurements = Measurements(
        timestamp= '2035-08-01 00:00:00.000 -0300',
        wind_speed= '13.032743',
        power= '2161.2974',
        air_temperature= '23.85818'
    )

    with pytest.raises(HTTPException):
        uc.add_measurements(measurements=measurements, asset_id=313213)


# def test_update_product(db_session, product_on_db):
#     product = Product(
#         name='Camisa Mike',
#         slug='camisa-mike',
#         price=22.99,
#         stock=22
#     )

#     uc = ProductUseCases(db_session=db_session)
#     uc.update_product(id=product_on_db.id, product=product)

#     product_updated_on_db = db_session.query(ProductModel).filter_by(id=product_on_db.id).first()

#     assert product_updated_on_db is not None
#     assert product_updated_on_db.name == product.name
#     assert product_updated_on_db.slug == product.slug
#     assert product_updated_on_db.price == product.price
#     assert product_updated_on_db.stock == product.stock


# def test_update_product_invalid_id(db_session):
#     product = Product(
#         name='Camisa Mike',
#         slug='camisa-mike',
#         price=22.99,
#         stock=22
#     )

#     uc = ProductUseCases(db_session=db_session)

#     with pytest.raises(HTTPException):
#         uc.update_product(id=1, product=product)

# def test_delete_product(db_session, product_on_db):
#     uc = ProductUseCases(db_session=db_session)
#     uc.delete_product(id=product_on_db.id)

#     products_on_db = db_session.query(ProductModel).all()

#     assert len(products_on_db) == 0


# def test_delete_product_non_exist(db_session):
#     uc = ProductUseCases(db_session=db_session)
    
#     with pytest.raises(HTTPException):
#         uc.delete_product(id=1)


# def test_list_products_uc(db_session, products_on_db):
#     uc = ProductUseCases(db_session=db_session)
    
#     page = uc.list_products(page=1, size=2)

#     assert type(page) == Page
#     assert len(page.items) == 2
#     assert page.total == 4
#     assert page.page == 1
#     assert page.size == 2
#     assert page.pages == 2

#     assert page.items[0].name == products_on_db[0].name
#     assert page.items[0].category.name == products_on_db[0].category.name


# def test_list_products_uc_with_search(db_session, products_on_db):
#     uc = ProductUseCases(db_session=db_session)
    
#     page = uc.list_products(search='mike')
    
#     assert type(page) == Page
#     assert len(page.items) == 3
#     assert page.items[0].name == products_on_db[0].name
#     assert page.items[0].category.name == products_on_db[0].category.name


def test_list_avarage_uc_with_specific_column(db_session, measurements_on_db):
    uc = MeasurementsUseCases(db_session=db_session)
    
    avarage = uc.list_average_value_(specific_column='power', asset_id=102, timestamp='2035-08-01 01:20:00.000 -0300')

    print(avarage) 