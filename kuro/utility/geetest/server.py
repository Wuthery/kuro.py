"""Simple geetest server implementation for solving captcha and entering data."""

import asyncio
import typing
import webbrowser

import aiohttp
from aiohttp import web

from ... import types
from ...models import MMTResult
from .utility import lang_to_geetest_lang

__all__ = ["PAGES", "enter_code", "launch_server", "solve_geetest"]

PAGES: typing.Final[dict[typing.Literal["captcha", "enter-code"], str]] = {
    "captcha": """
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
              captchaId: "ec4aa4174277d822d73f2442a165a2cd", // Hardcoded by kuro
              product: "bind",
              language: "{lang}",
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
    """,
    "enter-code": """
    <!DOCTYPE html>
    <html>
      <body>
        <input id="code" type="number">
        <button id="verify">Send</button>
      </body>
      <script>
        document.getElementById("verify").onclick = () => {
          fetch("/send-data", {
            method: "POST",
            body: JSON.stringify({
              code: document.getElementById("code").value
            }),
          });
          document.body.innerHTML = "You may now close this window.";
        };
      </script>
    </html>
    """,
}

GT_URL = "https://static.geetest.com/v4/gt4.js"


@typing.overload
async def launch_server(
    page: typing.Literal["captcha"],
    *,
    lang: str = ...,
    port: int = ...,
) -> MMTResult: ...
@typing.overload
async def launch_server(
    page: typing.Literal["enter-code"],
    *,
    lang: None = ...,
    port: int = ...,
) -> str: ...
async def launch_server(
    page: typing.Literal["captcha", "enter-code"],
    *,
    lang: str | None = None,
    port: int = 5000,
) -> MMTResult | str:
    """Create and run a web server to solve captcha or enter a verification code."""
    routes = web.RouteTableDef()
    future: asyncio.Future[typing.Any] = asyncio.Future()

    @routes.get("/")
    async def index(request: web.Request) -> web.StreamResponse:
        body = PAGES[page]
        body = body.replace("{lang}", lang or "en")
        return web.Response(body=body, content_type="text/html")

    @routes.get("/gt.js")
    async def gt(request: web.Request) -> web.StreamResponse:
        async with aiohttp.ClientSession() as session:
            r = await session.get(GT_URL)
            content = await r.read()

        return web.Response(body=content, content_type="text/javascript")

    @routes.post("/send-data")
    async def send_data_endpoint(request: web.Request) -> web.Response:
        result = await request.json()
        result = result.get("code", MMTResult(**result))
        future.set_result(result)
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
    *,
    lang: str = types.Lang,
    port: int = 5000,
) -> MMTResult:
    """Start a web server and manually solve geetest captcha."""
    lang = lang_to_geetest_lang(lang)
    return await launch_server(
        "captcha",
        lang=lang,
        port=port,
    )


async def enter_code(*, port: int = 5000) -> str:
    """Get email or phone number verification code from user."""
    return await launch_server("enter-code", port=port)
