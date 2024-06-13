import kuro
from kuro.utility.gacha import parse_gacha_url


def test_url_parser(gacha_url: str):
    """Test gacha url parser."""
    parsed = parse_gacha_url(gacha_url)

    assert parsed["player_id"] == 600435095
    assert parsed["record_id"] == "fd446edbbea412bf1947ebfcf408accb"
    assert parsed["server"] == "6eb2a235b30d05efd77bedb5cf60999e"
    assert parsed["banner"] == kuro.types.WuWaBanner(6)
    assert parsed["lang"] == kuro.types.Lang("en")
