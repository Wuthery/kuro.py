from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kuro


async def test_game_announcements(client: "kuro.Client"):
    """Test game announcements."""
    announcements = await client.get_game_announcements()

    assert len(announcements.game) > 0
    assert len(announcements.event) > 0


async def test_cn_game_announcements(cn_client: "kuro.Client"):
    """Test CN game announcements."""
    announcements = await cn_client.get_game_announcements()

    assert len(announcements.game) > 0
    assert len(announcements.event) > 0


async def test_game_announcement_details(client: "kuro.Client"):
    """Test game announcements details."""
    announcements = await client.get_game_announcements()
    announcement_id = announcements.game[0].id

    announcement_details = await client.get_game_announcement_details(announcement_id)
    assert str(announcement_details.announcement_id) == announcement_id


async def test_cn_game_announcement_details(cn_client: "kuro.Client"):
    """Test CN game announcements details."""
    announcements = await cn_client.get_game_announcements()
    announcement_id = announcements.game[0].id

    announcement_details = await cn_client.get_game_announcement_details(announcement_id)
    assert str(announcement_details.announcement_id) == announcement_id


async def test_launcher_announcements(client: "kuro.Client"):
    """Test launcher announcements."""
    announcements = await client.get_launcher_announcements()

    assert len(announcements.guidance.notice.contents) > 0
    assert len(announcements.guidance.news.contents) > 0


async def test_cn_launcher_announcements(cn_client: "kuro.Client"):
    """Test CN launcher announcements."""
    announcements = await cn_client.get_launcher_announcements()

    assert len(announcements.guidance.notice.contents) > 0
    assert len(announcements.guidance.activity.contents) > 0
    assert len(announcements.guidance.news.contents) > 0


async def test_launcher_announcements_details(client: "kuro.Client"):
    """Test launcher announcements details."""
    announcements = await client.get_launcher_announcements()

    notice_article_id = announcements.guidance.notice.contents[0].id
    announcement_details = await client.get_launcher_announcement_details(notice_article_id)
    assert announcement_details.article_id == notice_article_id

    news_article_id = announcements.guidance.news.contents[0].id
    announcement_details = await client.get_launcher_announcement_details(news_article_id)
    assert announcement_details.article_id == news_article_id
