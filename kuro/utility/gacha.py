"""Gacha utility."""

from urllib.parse import parse_qs, urlparse

from kuro import models, types


def parse_gacha_url(url: str) -> models.ParsedGachaParams:
    """Parse gacha URL.

    Use the function to parse gacha url into a mapping that can be
    ued in `client.get_gacha_records` method:

    ```python
    url = "..."
    parsed = parse_gacha_url(url)
    records = await client.get_gacha_records(**parsed)
    ```

    Args:
        url: URL to parse.

    Returns:
        Parsed mapping that can be used in `client.get_gacha_records` method.
    """
    parsed_url = urlparse(url.replace("#", ""))
    query_params = parse_qs(parsed_url.query)
    return {
        "player_id": int(query_params["player_id"][0]),
        "record_id": query_params["record_id"][0],
        "server": types.WuWaServer(query_params["svr_id"][0]),
        "banner": types.WuWaBanner(int(query_params["gacha_type"][0])),
        "lang": types.Lang(query_params["lang"][0]),
    }
