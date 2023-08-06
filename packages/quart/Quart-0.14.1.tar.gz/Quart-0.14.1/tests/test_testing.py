from typing import Callable, Optional

import pytest
from werkzeug.datastructures import Headers

from quart import jsonify, Quart, redirect, request, Response, session, websocket
from quart.testing import (
    make_test_body_with_headers,
    make_test_headers_path_and_query_string,
    QuartClient as Client,
    WebsocketResponse,
)


@pytest.mark.asyncio
async def test_methods() -> None:
    app = Quart(__name__)

    methods = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"]

    @app.route("/", methods=methods)
    async def echo() -> str:
        return request.method

    client = Client(app)

    for method in methods:
        func = getattr(client, method.lower())
        response = await func("/")
        assert method in (await response.get_data(raw=False))


@pytest.mark.parametrize(
    "path, query_string, expected_path, expected_query_string",
    [
        ("/path", {"a": "b"}, "/path", b"a=b"),
        ("/path", {"a": ["b", "c"]}, "/path", b"a=b&a=c"),
        ("/path?b=c", None, "/path", b"b=c"),
        ("/path%20", None, "/path ", b""),
    ],
)
def test_build_headers_path_and_query_string(
    path: str, query_string: Optional[dict], expected_path: str, expected_query_string: bytes
) -> None:
    headers, result_path, result_qs = make_test_headers_path_and_query_string(
        Quart(__name__), path, None, query_string
    )
    assert result_path == expected_path
    assert headers["Remote-Addr"] == "127.0.0.1"
    assert headers["User-Agent"] == "Quart"
    assert headers["host"] == "localhost"
    assert result_qs == expected_query_string


def test_build_headers_path_and_query_string_with_query_string_error() -> None:
    with pytest.raises(ValueError):
        make_test_headers_path_and_query_string(Quart(__name__), "/?a=b", None, {"c": "d"})


def test_make_test_body_with_headers_data() -> None:
    body, headers = make_test_body_with_headers(data="data")
    assert body == b"data"
    assert headers == Headers()


def test_make_test_body_with_headers_form() -> None:
    body, headers = make_test_body_with_headers(form={"a": "b"})
    assert body == b"a=b"
    assert headers == Headers({"Content-Type": "application/x-www-form-urlencoded"})


def test_make_test_body_with_headers_json() -> None:
    body, headers = make_test_body_with_headers(json={"a": "b"})
    assert body == b'{"a": "b"}'
    assert headers == Headers({"Content-Type": "application/json"})


def test_make_test_body_with_headers_argument_error() -> None:
    with pytest.raises(ValueError):
        make_test_body_with_headers(json={}, data="", form={})


@pytest.mark.parametrize(
    "headers, expected",
    [
        (None, Headers({"Remote-Addr": "127.0.0.1", "User-Agent": "Quart", "host": "localhost"})),
        (
            Headers({"Remote-Addr": "1.2.3.4", "User-Agent": "Quarty", "host": "quart.com"}),
            Headers({"Remote-Addr": "1.2.3.4", "User-Agent": "Quarty", "host": "quart.com"}),
        ),
    ],
)
def test_build_headers_path_and_query_string_headers_defaults(
    headers: Headers, expected: Headers
) -> None:
    result, path, query_string = make_test_headers_path_and_query_string(
        Quart(__name__), "/path", headers
    )
    assert result == expected
    assert path == "/path"
    assert query_string == b""


@pytest.mark.asyncio
async def test_json() -> None:
    app = Quart(__name__)

    @app.route("/", methods=["POST"])
    async def echo() -> Response:
        data = await request.get_json()
        return jsonify(data)

    client = Client(app)
    response = await client.post("/", json={"a": "b"})
    assert (await response.get_json()) == {"a": "b"}


@pytest.mark.asyncio
async def test_form() -> None:
    app = Quart(__name__)

    @app.route("/", methods=["POST"])
    async def echo() -> Response:
        data = await request.form
        return jsonify(**data)

    client = Client(app)
    response = await client.post("/", form={"a": "b"})
    assert (await response.get_json()) == {"a": "b"}


@pytest.mark.asyncio
async def test_data() -> None:
    app = Quart(__name__)

    @app.route("/", methods=["POST"])
    async def echo() -> Response:
        data = await request.get_data(True)
        return data

    client = Client(app)
    headers = {"Content-Type": "application/octet-stream"}
    response = await client.post("/", data=b"ABCDEFG", headers=headers)
    assert (await response.get_data(True)) == b"ABCDEFG"


@pytest.mark.asyncio
async def test_query_string() -> None:
    app = Quart(__name__)

    @app.route("/", methods=["GET"])
    async def echo() -> Response:
        data = request.args
        return jsonify(**data)

    client = Client(app)
    response = await client.get("/", query_string={"a": "b"})
    assert (await response.get_json()) == {"a": "b"}


@pytest.mark.asyncio
async def test_redirect() -> None:
    app = Quart(__name__)

    @app.route("/", methods=["GET"])
    async def echo() -> str:
        return request.method

    @app.route("/redirect", methods=["GET"])
    async def redir() -> Response:
        return redirect("/")

    client = Client(app)
    assert (await client.get("/redirect", follow_redirects=True)).status_code == 200


@pytest.mark.asyncio
async def test_cookie_jar() -> None:
    app = Quart(__name__)
    app.secret_key = "secret"

    @app.route("/", methods=["GET"])
    async def echo() -> Response:
        foo = session.get("foo")
        bar = request.cookies.get("bar")
        session["foo"] = "bar"
        response = jsonify({"foo": foo, "bar": bar})
        response.set_cookie("bar", "foo")
        return response

    client = Client(app)
    response = await client.get("/")
    assert (await response.get_json()) == {"foo": None, "bar": None}
    response = await client.get("/")
    assert (await response.get_json()) == {"foo": "bar", "bar": "foo"}


@pytest.mark.asyncio
async def test_redirect_cookie_jar() -> None:
    app = Quart(__name__)
    app.secret_key = "secret"

    @app.route("/a")
    async def a() -> Response:
        response = redirect("/b")
        response.set_cookie("bar", "foo")
        return response

    @app.route("/b")
    async def echo() -> Response:
        bar = request.cookies.get("bar")
        response = jsonify({"bar": bar})
        return response

    client = Client(app)
    response = await client.get("/a", follow_redirects=True)
    assert (await response.get_json()) == {"bar": "foo"}


@pytest.mark.asyncio
async def test_set_cookie() -> None:
    app = Quart(__name__)

    @app.route("/", methods=["GET"])
    async def echo() -> Response:
        return jsonify({"foo": request.cookies.get("foo")})

    client = Client(app)
    client.set_cookie("localhost", "foo", "bar")
    response = await client.get("/")
    assert (await response.get_json()) == {"foo": "bar"}


@pytest.mark.asyncio
async def test_websocket_bad_request() -> None:
    app = Quart(__name__)

    @app.route("/")
    async def index() -> str:
        return ""

    test_client = app.test_client()
    with pytest.raises(WebsocketResponse):
        async with test_client.websocket("/"):
            pass


@pytest.mark.asyncio
async def test_push_promise() -> None:
    app = Quart(__name__)

    @app.route("/")
    async def index() -> str:
        await request.send_push_promise("/")
        return ""

    test_client = app.test_client()
    await test_client.get("/", http_version="2")
    assert test_client.push_promises[0][0] == "/"


@pytest.mark.asyncio
async def test_session_transactions() -> None:
    app = Quart(__name__)
    app.secret_key = "secret"

    @app.route("/")
    async def index() -> str:
        return str(session["foo"])

    test_client = app.test_client()

    async with test_client.session_transaction() as local_session:
        assert len(local_session) == 0
        local_session["foo"] = [42]
        assert len(local_session) == 1
    response = await test_client.get("/")
    assert (await response.get_data()) == b"[42]"  # type: ignore
    async with test_client.session_transaction() as local_session:
        assert len(local_session) == 1
        assert local_session["foo"] == [42]


@pytest.mark.asyncio
async def test_with_usage() -> None:
    app = Quart(__name__)
    app.secret_key = "secret"

    @app.route("/")
    async def index() -> str:
        session["hello"] = "world"
        return "Hello"

    async with app.test_client() as client:
        await client.get("/")
        assert request.method == "GET"
        assert session["hello"] == "world"


@pytest.mark.asyncio
async def test_websocket_json() -> None:
    app = Quart(__name__)

    @app.websocket("/ws/")
    async def ws() -> None:
        data = await websocket.receive_json()
        await websocket.send_json(data)

    async with app.test_client().websocket("/ws/") as test_websocket:
        await test_websocket.send_json({"foo": "bar"})
        data = await test_websocket.receive_json()
        assert data == {"foo": "bar"}


@pytest.mark.asyncio
async def test_middleware() -> None:
    app = Quart(__name__)

    @app.route("/")
    async def index() -> str:
        return "Hello"

    class OddMiddleware:
        def __init__(self, app: Callable) -> None:
            self.app = app

        async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
            if scope["path"] != "/":
                await send(
                    {
                        "type": "http.response.start",
                        "status": 401,
                        "headers": [(b"content-length", b"0")],
                    }
                )
                await send(
                    {
                        "type": "http.response.body",
                        "body": b"",
                        "more_body": False,
                    }
                )
            else:
                await self.app(scope, receive, send)

    app.asgi_app = OddMiddleware(app.asgi_app)  # type: ignore

    client = app.test_client()
    response = await client.get("/")
    assert response.status_code == 200
    response = await client.get("/odd")
    assert response.status_code == 401
