from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kuro


async def test_game_user(client: "kuro.Client", email: str, password: str):
    """Test game user info."""
    login_result = await client.game_login(email, password)
    token_result = await client.get_game_token(login_result.code)

    user = await client.get_game_user(
        login_result.id, token_result.access_token, "UA", login_result.username
    )

    assert user.id == login_result.id
    assert user.sdk_login_code != 0
