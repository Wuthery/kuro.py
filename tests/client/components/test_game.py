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


async def test_game_player_info(client: "kuro.Client", email: str, password: str):
    """Test game player info."""
    login_result = await client.game_login(email, password)
    token_result = await client.get_game_token(login_result.code)
    oauth_code = await client.generate_oauth_code(token_result.access_token)

    player_info = await client.get_player_info(oauth_code)

    for info in player_info.values():
        assert info.level >= 1


async def test_game_player_role(client: "kuro.Client", email: str, password: str):
    """Test game player role."""
    login_result = await client.game_login(email, password)
    token_result = await client.get_game_token(login_result.code)
    oauth_code = await client.generate_oauth_code(token_result.access_token)

    player_info = await client.get_player_info(oauth_code)

    first_region = next(iter(player_info))
    first_player_id = player_info[first_region].uid

    role_info = await client.get_player_role(oauth_code, first_player_id, first_region)

    assert role_info.basic.id == first_player_id
