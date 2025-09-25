"""Simple geetest server implementation for solving captcha."""

from __future__ import annotations

import asyncio
import typing
import webbrowser

import aiohttp
from aiohttp import web

from kuro import models, types
from kuro.utility import geetest

__all__ = ["PAGE", "launch_server", "solve_geetest"]

PAGE = """
<!DOCTYPE html>
<head>
  <meta name="referrer" content="no-referrer"/>
</head>
<html>
  <body></body>
  <script src="./gt.js"></script>
  <script>
      window.initGeetest4(
        {
          captchaId: "%s",
          product: "bind",
          language: "%s",
        },
        (captcha) => {
          captcha.onReady(() => {
            captcha.showCaptcha();
          });
          captcha.onSuccess(() => {
            fetch("/send-data", {
              method: "POST",
              body: JSON.stringify(captcha.getValidate()),
            }).then(() => window.close());
            document.body.innerHTML = "You may now close this window.";
          });
        }
      )
  </script>
</html>
"""

GT_URL = "https://static.geetest.com/v4/gt4.js"


async def launch_server(*, captcha_id: str, lang: str, port: int = 5000) -> models.MMTResult:
    """Create and run a web server to solve captcha."""
    routes = web.RouteTableDef()
    future: asyncio.Future[typing.Any] = asyncio.Future()

    @routes.get("/")
    async def index(_: web.Request) -> web.StreamResponse:  # noqa: RUF029
        body = PAGE % (str(captcha_id), lang or "en")
        return web.Response(body=body, content_type="text/html")

    @routes.get("/gt.js")
    async def gt(_: web.Request) -> web.StreamResponse:
        async with aiohttp.ClientSession() as session:
            r = await session.get(GT_URL)
            content = await r.read()

        return web.Response(body=content, content_type="text/javascript")

    @routes.post("/send-data")
    async def send_data_endpoint(request: web.Request) -> web.Response:
        result = await request.json()
        future.set_result(models.MMTResult(**result))
        return web.Response(status=204)

    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, host="localhost", port=port)
    print(f"Opening http://localhost:{port} in browser...")  # noqa
    webbrowser.open_new_tab(f"http://localhost:{port}")

    await site.start()

    try:
        data = await future
    finally:
        await asyncio.sleep(0.3)
        await runner.shutdown()
        await runner.cleanup()

    return data


async def solve_geetest(
    *, captcha_id: types.CaptchaId | str, lang: types.Lang, port: int = 5000
) -> models.MMTResult:
    """Start a web server and manually solve geetest captcha."""
    geetest_lang = geetest.lang_to_geetest_lang(lang)
    captcha_id_str = captcha_id.value if isinstance(captcha_id, types.CaptchaId) else captcha_id
    return await launch_server(captcha_id=captcha_id_str, lang=geetest_lang, port=port)
