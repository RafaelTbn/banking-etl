import aiohttp
import asyncio

class FetchError(Exception):
    pass

def retry(retries=3, delay=1):
    def wrapper(func):
        async def inner(*args, **kwargs):
            last = None
            for _ in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last = e
                    await asyncio.sleep(delay)
            raise FetchError(str(last))
        return inner
    return wrapper

@retry()
async def fetch_quote(symbol: str) -> dict:
    url = "https://dummyjson.com/quotes/random"
    timeout = aiohttp.ClientTimeout(total=5)

    async with aiohttp.ClientSession(timeout=timeout) as sess:
        async with sess.get(url) as resp:
            if resp.status != 200:
                raise FetchError(f"Bad status: {resp.status}")
            return await resp.json()
