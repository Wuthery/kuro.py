from typing import TYPE_CHECKING

from kuro.utility.auth import generate_uuid_uppercase

if TYPE_CHECKING:
    import kuro


async def test_game_login(client: "kuro.Client", email: str, password: str):
    """Test game login."""
    login_result = await client.game_login(email, password)

    assert login_result.email == email
    assert not login_result.first_login


async def test_get_game_token(client: "kuro.Client", email: str, password: str):
    """Test obtaining game token."""
    login_result = await client.game_login(email, password)
    token_result = await client.get_game_token(login_result.code)

    assert token_result.access_token
    assert token_result.expires_in >= 250000


async def test_check_game_token(client: "kuro.Client", email: str, password: str):
    """Test checking game token."""
    login_result = await client.game_login(email, password)
    token_result = await client.get_game_token(login_result.code)
    expires_in = await client.check_game_token(token_result.access_token)

    assert expires_in >= 250000


async def test_game_auto_login(client: "kuro.Client", email: str, password: str):
    """Test game auto login."""
    device_id = generate_uuid_uppercase()
    login_result = await client.game_login(email, password, device_id=device_id)
    auto_login_result = await client.game_auto_login(login_result.auto_token, device_id=device_id)

    assert auto_login_result.email == email
    assert not auto_login_result.first_login


async def test_oauth_code(client: "kuro.Client", email: str, password: str):
    """Test obtaining OAuth code."""
    login_result = await client.game_login(email, password)
    token_result = await client.get_game_token(login_result.code)
    oauth_code = await client.generate_oauth_code(token_result.access_token)

    assert oauth_code
