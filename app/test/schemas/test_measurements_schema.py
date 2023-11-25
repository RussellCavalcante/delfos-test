import pytest
from app.schemas.measurements import Measurements, MeasurementsInput, MeasurementsOutput
from app.schemas.assets import Asset


def test_measurements_schema():
    measurements = Measurements(
        timestamp= '2035-08-01 00:00:00.000 -0300',
        wind_speed= '13.032743',
        power= '2161.2974',
        air_temperature= '23.85818'
    )

    assert measurements.dict() == {
        'timestamp':'2035-08-01 00:00:00.000 -0300',
        'wind_speed': '13.032743',
        'power': '2161.2974',
        'air_temperature': '23.85818'
    }

def test_measurements_schema_invalid():
    with pytest.raises(ValueError):
        measurements = Measurements(
            timestamp= '2035-08-01 00:00:00.000 -0300',
            wind_speed= '13.032743',
            power= '2161.2974',
            air_temperature= 12121
        )



def test_measurements_input_schema():
    measurements = Measurements(
        timestamp= '2035-08-01 00:00:00.000 -0300',
        wind_speed= '13.032743',
        power= '2161.2974',
        air_temperature= '23.85818'
    )
    
    measurements_input = MeasurementsInput(
        asset_id='101',
        measurements=measurements
    )

    assert measurements_input.dict() == {
        "asset_id": 101,
        "measurements": {
            "timestamp": "2035-08-01 00:00:00.000 -0300",
            "wind_speed": "13.032743",
            "power": "2161.2974",
            "air_temperature": "23.85818"
        }
    }


def test_measurements_output_schema():
    asset = Asset(id = 101, name = "WTG 101",)

    measurements_output = MeasurementsOutput(
        id=101,
        timestamp = "2035-08-01 00:00:00.000 -0300",
        wind_speed = "13.032743",
        power = "2161.2974",
        air_temperature = "23.85818",
        asset = asset
    )
    print(measurements_output.dict())

    assert measurements_output.dict() == {
        "id": 101,
        "timestamp": "2035-08-01 00:00:00.000 -0300",
        "wind_speed": "13.032743",
        "power": "2161.2974",
        "air_temperature": "23.85818",
        "asset": {
            "id": 101,
            "name": "WTG 101",
        }
    }
