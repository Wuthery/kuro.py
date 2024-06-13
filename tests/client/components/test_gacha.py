import kuro
from kuro.utility.gacha import parse_gacha_url


async def test_gacha_records(client: kuro.Client, gacha_url: str):
    """Test gacha records."""
    parsed = parse_gacha_url(gacha_url)
    parsed["banner"] = kuro.types.WuWaBanner(2)

    records = await client.get_gacha_record(**parsed)

    assert records[0].banner == kuro.types.WuWaBanner(2)
    assert records[0].count == 1
