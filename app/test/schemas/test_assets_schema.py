import pytest
from app.schemas.assets import Asset


def test_asset_schema():
    asset = Asset(
        id=101,
        name='WTG 01'
    )

    assert asset.dict() == {
        'id': 101,
        'name': 'WTG 01'
    }


def test_asset_schema_invalid():
    with pytest.raises(ValueError):
         asset = Asset(
            id="wtg",
            name='WTG 01'
        )

    with pytest.raises(ValueError):
        asset = Asset(
            id="wtg",
            name=1
        )
    
    with pytest.raises(ValueError):
        asset = Asset(
            id=1,
            name=1
        )
