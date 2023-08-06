import asyncio
from typing import cast
from unittest.mock import Mock

import pytest
from werkzeug.datastructures import Headers
from werkzeug.exceptions import (
    BadRequest as WBadRequest,
    MethodNotAllowed as WMethodNotAllowed,
    NotFound as WNotFound,
)
from werkzeug.routing import RequestRedirect as WRequestRedirect

from quart.app import Quart
from quart.ctx import (
    _AppCtxGlobals,
    after_this_request,
    AppContext,
    copy_current_app_context,
    copy_current_request_context,
    copy_current_websocket_context,
    has_app_context,
    has_request_context,
    RequestContext,
)
from quart.exceptions import BadRequest, MethodNotAllowed, NotFound, RedirectRequired
from quart.globals import g, request, websocket
from quart.routing import QuartRule
from quart.testing import make_test_headers_path_and_query_string, no_op_push
from quart.wrappers import Request, Websocket


def test_request_context_match() -> None:
    app = Quart(__name__)
    url_adapter = Mock()
    rule = QuartRule("/", methods={"GET"}, endpoint="index")
    url_adapter.match.return_value = (rule, {"arg": "value"})
    app.create_url_adapter = lambda *_: url_adapter  # type: ignore
    request = Request(
        "GET",
        "http",
        "/",
        b"",
        Headers([("host", "quart.com")]),
        "",
        "1.1",
        {},
        send_push_promise=no_op_push,
    )
    RequestContext(app, request)
    assert request.url_rule == rule
    assert request.view_args == {"arg": "value"}


@pytest.mark.parametrize(
    "exception_type, exception_instance",
    [
        (BadRequest, WBadRequest()),
        (MethodNotAllowed, WMethodNotAllowed(["GET"])),
        (NotFound, WNotFound()),
        (RedirectRequired, WRequestRedirect("/")),
    ],
)
def test_request_context_matching_error(
    exception_type: Exception, exception_instance: Exception
) -> None:
    app = Quart(__name__)
    url_adapter = Mock()
    url_adapter.match.side_effect = exception_instance
    app.create_url_adapter = lambda *_: url_adapter  # type: ignore
    request = Request(
        "GET",
        "http",
        "/",
        b"",
        Headers([("host", "quart.com")]),
        "",
        "1.1",
        {},
        send_push_promise=no_op_push,
    )
    RequestContext(app, request)
    assert isinstance(request.routing_exception, exception_type)  # type: ignore


def test_bad_request_if_websocket_route() -> None:
    app = Quart(__name__)
    url_adapter = Mock()
    url_adapter.match.side_effect = WBadRequest()
    app.create_url_adapter = lambda *_: url_adapter  # type: ignore
    request = Request(
        "GET",
        "http",
        "/",
        b"",
        Headers([("host", "quart.com")]),
        "",
        "1.1",
        {},
        send_push_promise=no_op_push,
    )
    RequestContext(app, request)
    assert isinstance(request.routing_exception, BadRequest)


@pytest.mark.asyncio
async def test_after_this_request() -> None:
    app = Quart(__name__)
    headers, path, query_string = make_test_headers_path_and_query_string(app, "/")
    async with RequestContext(
        Quart(__name__),
        Request(
            "GET", "http", path, query_string, headers, "", "1.1", {}, send_push_promise=no_op_push
        ),
    ) as context:
        after_this_request(lambda: "hello")
        assert context._after_request_functions[0]() == "hello"


@pytest.mark.asyncio
async def test_has_request_context() -> None:
    app = Quart(__name__)
    headers, path, query_string = make_test_headers_path_and_query_string(app, "/")
    request = Request(
        "GET", "http", path, query_string, headers, "", "1.1", {}, send_push_promise=no_op_push
    )
    async with RequestContext(Quart(__name__), request):
        assert has_request_context() is True
        assert has_app_context() is True
    assert has_request_context() is False
    assert has_app_context() is False


@pytest.mark.asyncio
async def test_has_app_context() -> None:
    async with AppContext(Quart(__name__)):
        assert has_app_context() is True
    assert has_app_context() is False


def test_app_ctx_globals_get() -> None:
    g = _AppCtxGlobals()
    g.foo = "bar"  # type: ignore
    assert g.get("foo") == "bar"
    assert g.get("bar", "something") == "something"


def test_app_ctx_globals_pop() -> None:
    g = _AppCtxGlobals()
    g.foo = "bar"  # type: ignore
    assert g.pop("foo") == "bar"
    assert g.pop("foo", None) is None
    with pytest.raises(KeyError):
        g.pop("foo")


def test_app_ctx_globals_setdefault() -> None:
    g = _AppCtxGlobals()
    g.setdefault("foo", []).append("bar")
    assert g.foo == ["bar"]  # type: ignore


def test_app_ctx_globals_contains() -> None:
    g = _AppCtxGlobals()
    g.foo = "bar"  # type: ignore
    assert "foo" in g
    assert "bar" not in g


def test_app_ctx_globals_iter() -> None:
    g = _AppCtxGlobals()
    g.foo = "bar"  # type: ignore
    g.bar = "foo"  # type: ignore
    assert sorted(iter(g)) == ["bar", "foo"]


@pytest.mark.asyncio
async def test_copy_current_app_context() -> None:
    app = Quart(__name__)

    @app.route("/")
    async def index() -> str:
        g.foo = "bar"  # type: ignore

        @copy_current_app_context
        async def within_context() -> None:
            assert g.foo == "bar"

        await asyncio.ensure_future(within_context())
        return ""

    test_client = app.test_client()
    response = await test_client.get("/")
    assert response.status_code == 200


def test_copy_current_app_context_error() -> None:
    with pytest.raises(RuntimeError):
        copy_current_app_context(lambda: None)()


@pytest.mark.asyncio
async def test_copy_current_request_context() -> None:
    app = Quart(__name__)

    @app.route("/")
    async def index() -> str:
        @copy_current_request_context
        async def within_context() -> None:
            assert request.path == "/"

        await asyncio.ensure_future(within_context())
        return ""

    test_client = app.test_client()
    response = await test_client.get("/")
    assert response.status_code == 200


def test_copy_current_request_context_error() -> None:
    with pytest.raises(RuntimeError):
        copy_current_request_context(lambda: None)()


@pytest.mark.asyncio
async def test_works_without_copy_current_request_context() -> None:
    app = Quart(__name__)

    @app.route("/")
    async def index() -> str:
        async def within_context() -> None:
            assert request.path == "/"

        await asyncio.ensure_future(within_context())
        return ""

    test_client = app.test_client()
    response = await test_client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_copy_current_websocket_context() -> None:
    app = Quart(__name__)

    @app.websocket("/")
    async def index() -> None:
        @copy_current_websocket_context
        async def within_context() -> None:
            return websocket.path

        data = await asyncio.ensure_future(within_context())
        await websocket.send(data.encode())

    test_client = app.test_client()
    async with test_client.websocket("/") as test_websocket:
        data = await test_websocket.receive()
    assert cast(bytes, data) == b"/"


def test_copy_current_websocket_context_error() -> None:
    with pytest.raises(RuntimeError):
        copy_current_websocket_context(lambda: None)()


@pytest.mark.asyncio
async def test_overlapping_request_ctx() -> None:
    app = Quart(__name__)

    request = Request(
        "GET",
        "http",
        "/",
        b"",
        Headers([("host", "quart.com")]),
        "",
        "1.1",
        {},
        send_push_promise=no_op_push,
    )
    ctx1 = app.request_context(request)
    await ctx1.__aenter__()
    ctx2 = app.request_context(request)
    await ctx2.__aenter__()
    await ctx1.__aexit__(None, None, None)
    assert has_app_context()  # Ensure the app context still exists for ctx2
    await ctx2.__aexit__(None, None, None)


@pytest.mark.asyncio
async def test_overlapping_websocket_ctx() -> None:
    app = Quart(__name__)

    websocket = Websocket(
        "/", b"", "ws", Headers([("host", "quart.com")]), "", "1.1", [], None, None, None, {}
    )
    ctx1 = app.websocket_context(websocket)
    await ctx1.__aenter__()
    ctx2 = app.websocket_context(websocket)
    await ctx2.__aenter__()
    await ctx1.__aexit__(None, None, None)
    assert has_app_context()  # Ensure the app context still exists for ctx2
    await ctx2.__aexit__(None, None, None)
