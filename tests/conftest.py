import os

import dotenv
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


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest."""
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def email() -> str:
    """Return the test login."""
    test_email = os.environ.get("TEST_EMAIL")
    if test_email is None:
        pytest.exit("Test email not set.", 1)

    return test_email


@pytest.fixture(scope="session")
def password() -> str:
    """Return the test password."""
    test_password = os.environ.get("TEST_PASSWORD")
    if test_password is None:
        pytest.exit("Test password not set.", 1)

    return test_password
