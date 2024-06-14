from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kuro


async def test_announcements(client: "kuro.Client"):
    """Test gacha records."""
    game_announcement_list = (await client.get_game_announcements()).game
    assert game_announcement_list


async def test_announcement_details(client: "kuro.Client"):
    """Test announcement_details."""
    game_announcement_list = (await client.get_game_announcements()).game

    # test for id method, then url
    game_announcement_detail = await client.get_game_announcement_details(
        game_announcement_list[0].id
    )
    assert game_announcement_detail

    game_announcement_detail = await client.get_game_announcement_details(
        url=game_announcement_list[0].details_url
    )
    assert game_announcement_detail
