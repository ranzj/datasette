from datasette.utils.asgi import Request
import pytest


@pytest.mark.asyncio
async def test_request_post_vars():
    scope = {
        "http_version": "1.1",
        "method": "POST",
        "path": "/",
        "raw_path": b"/",
        "query_string": b"",
        "scheme": "http",
        "type": "http",
        "headers": [[b"content-type", b"application/x-www-form-urlencoded"]],
    }

    async def receive():
        return {"type": "http.request", "body": b"foo=bar&baz=1", "more_body": False}

    request = Request(scope, receive)
    assert {"foo": "bar", "baz": "1"} == await request.post_vars()


def test_request_args():
    request = Request.fake("/foo?multi=1&multi=2&single=3")
    assert "1" == request.args.get("multi")
    assert "3" == request.args.get("single")
    assert "1" == request.args["multi"]
    assert "3" == request.args["single"]
    assert ["1", "2"] == request.args.getlist("multi")
    assert [] == request.args.getlist("missing")
    assert "multi" in request.args
    assert "single" in request.args
    assert "missing" not in request.args
    expected = ["multi", "single"]
    assert expected == list(request.args.keys())
    for i, key in enumerate(request.args):
        assert expected[i] == key
    assert 2 == len(request.args)
    with pytest.raises(KeyError):
        request.args["missing"]
