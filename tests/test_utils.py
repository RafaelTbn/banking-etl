import pytest
from unittest.mock import AsyncMock, patch
from utils.async_api import fetch_quote

@pytest.mark.asyncio
async def test_async_api_call():
    class MockResponse:
        status = 200
        json = AsyncMock(return_value={"quote": "hello"})

    class GetCtx:
        async def __aenter__(self):
            return MockResponse()
        async def __aexit__(self, *a):
            pass

    class MockSession:
        def get(self, url):
            return GetCtx()
        async def __aenter__(self):
            return self
        async def __aexit__(self, *a):
            pass

    with patch("aiohttp.ClientSession", return_value=MockSession()):
        res = await fetch_quote("AAPL")
        assert res == {"quote": "hello"}
