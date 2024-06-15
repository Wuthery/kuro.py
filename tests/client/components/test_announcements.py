from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kuro


async def test_announcements(client: "kuro.Client"):
    """Test game announcements."""
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


async def test_kurobbs_announcements(client: "kuro.Client"):
    """Test kurobbs announcements."""
    kurobbs_announcements = await client.get_kurobbs_announcements()

    assert kurobbs_announcements


async def test_launcher_announcements(client: "kuro.Client"):
    """Test launcher announcements."""
    launcher_announcements = await client.get_launcher_announcements()

    assert launcher_announcements


async def test_launcher_details(client: "kuro.Client"):
    """Test Launcher announcement details."""
    launcher_announcements = await client.get_launcher_announcements()

    announcement_id = launcher_announcements.guidance.activity.contents[0].id
    lang = launcher_announcements.guidance.activity.contents[0].lang

    result = await client.get_launcher_announcement_details(announcement_id, lang)

    assert result
