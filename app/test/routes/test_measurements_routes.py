from fastapi.testclient import TestClient
from fastapi import status
from app.db.models import Measurement as MeasurementModel
from app.main import app


client = TestClient(app)
headers = {"Authorization": "Bearer token"}
client.headers = headers


def test_add_measurement_route(db_session, asset_on_db):
    body = {
        "asset_id": asset_on_db[0].id,
        "measurements": {
        "timestamp": "2035-08-01 00:00:00.000 -0300",
        "wind_speed": "13.032743",
        "power": "2161.2974",
        "air_temperature": "23.85818"
        }
    }

    response = client.post('/measurement/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    measurements_on_db = db_session.query(MeasurementModel).all()

    assert len(measurements_on_db) == 1

    db_session.delete(measurements_on_db[0])
    db_session.commit()


# def test_add_measurement_route_invalid_category_slug(db_session):
#     body = {
#         "category_slug": 'invalid',
#         "measurement": {
#             "name": "Camisa Mike",
#             "slug": "camisa-mike",
#             "price": 23.99,
#             "stock": 23
#         }
#     }

#     response = client.post('/measurement/add', json=body)

#     assert response.status_code == status.HTTP_404_NOT_FOUND

#     measurements_on_db = db_session.query(MeasurementModel).all()

#     assert len(measurements_on_db) == 0


# def test_update_measurement_route(db_session, measurement_on_db):
#     body = {
#         "name": "Updated camisa",
#         "slug": "updated-camisa",
#         "price": 23.88,
#         "stock": 10
#     }

#     response = client.put(f'/measurement/update/{measurement_on_db.id}', json=body)

#     assert response.status_code == status.HTTP_200_OK

#     db_session.refresh(measurement_on_db)
    
#     measurement_on_db.name == 'Updated camisa'
#     measurement_on_db.slug == 'updated-camisa'
#     measurement_on_db.price == 23.88
#     measurement_on_db.stock == 10


# def test_update_measurement_route_invalid_id():
#     body = {
#         "name": "Updated camisa",
#         "slug": "updated-camisa",
#         "price": 23.88,
#         "stock": 10
#     }

#     response = client.put(f'/measurement/update/1', json=body)

#     assert response.status_code == status.HTTP_404_NOT_FOUND


# def test_delete_measurement_route(db_session, measurement_on_db):
#     response = client.delete(f'/measurement/delete/{measurement_on_db.id}')

#     assert response.status_code == status.HTTP_200_OK

#     measurements_on_db = db_session.query(MeasurementModel).all()

#     assert len(measurements_on_db) == 0


# def test_delete_measurement_route_invalid_id():
#     response = client.delete(f'/measurement/delete/1')

#     assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_measurements_route(measurements_on_db):
    response = client.get('/measurement/list')
   
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    print(data)

    # assert 'items' in data
    # assert len(data['items']) == 4

    # assert data['items'][0] == {
    #     'id': measurements_on_db[0].id,
    #     'name': measurements_on_db[0].name,
    #     'slug': measurements_on_db[0].slug,
    #     'price': measurements_on_db[0].price,
    #     'stock': measurements_on_db[0].stock,
    #     'category': {
    #         'name': measurements_on_db[0].category.name,
    #         'slug': measurements_on_db[0].category.slug
    #     }
    # }

#     assert data['total'] == 4
#     assert data['page'] == 1
#     assert data['size'] == 50
#     assert data['pages'] == 1


def test_list_average_value_route(measurements_on_db):
    response = client.get('/measurement/list_average_value?timestamp=2035-08-01 01:20:00.000 -0300&specific_column=power&asset_id=102')
    print(response)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    print(data)


# def test_list_measurements_route_with_search(measurements_on_db):
#     response = client.get('/measurement/list?search=mike')

#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()

#     assert 'items' in data
#     assert len(data['items']) == 3

#     assert data['items'][0] == {
#         'id': measurements_on_db[0].id,
#         'name': measurements_on_db[0].name,
#         'slug': measurements_on_db[0].slug,
#         'price': measurements_on_db[0].price,
#         'stock': measurements_on_db[0].stock,
#         'category': {
#             'name': measurements_on_db[0].category.name,
#             'slug': measurements_on_db[0].category.slug
#         }
#     }

#     assert data['total'] == 3
#     assert data['page'] == 1
#     assert data['size'] == 50
#     assert data['pages'] == 1