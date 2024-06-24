import pytest

import kuro
from kuro import types


@pytest.fixture(scope="session")
async def client():
    """Return a Kuro client instance."""
    client = kuro.Client()
    client.debug = True

    return client


@pytest.fixture(scope="session")
async def cn_client():
    """Return a CN Kuro client instance."""
    client = kuro.Client(region=types.Region.CHINESE)
    client.debug = True

    return client


@pytest.fixture(scope="session")
def gacha_url():
    """Return a gacha URL."""
    return (
        "https://aki-gm-resources-oversea.aki-game.net/aki/gacha/index.html#/record?"
        "svr_id=6eb2a235b30d05efd77bedb5cf60999e"
        "&"
        "player_id=600435095"
        "&"
        "lang=en"
        "&"
        "gacha_id=4"
        "&"
        "gacha_type=6"
        "&"
        "svr_area=global"
        "&"
        "record_id=fd446edbbea412bf1947ebfcf408accb"
        "&"
        "resources_id=917dfa695d6c6634ee4e972bb9168f6a"
    )
