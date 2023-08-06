import aiohttp


class AsyncHttpRequest:
    @classmethod
    async def get(cls, url, redirect=True, params=None) -> any:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=str(url), allow_redirects=bool(redirect), params=params) as response:
                return response.url, await response.text('utf-8'), response.cookies

    @classmethod
    async def post(cls, url, data=None, json=None) -> any:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data, json=json) as response:
                return response.url, await response.text('utf-8'), response.cookies

    @classmethod
    async def put(cls, url, data=None) -> any:
        async with aiohttp.ClientSession() as session:
            async with session.put(url=url, data=data) as response:
                return response.url, await response.text('utf-8'), response.cookies

    @classmethod
    async def delete(cls, url) -> any:
        async with aiohttp.ClientSession() as session:
            async with session.delete(url=url) as response:
                return response.url, await response.text('utf-8'), response.cookies

    @classmethod
    async def head(cls, url, redirect=True) -> any:
        async with aiohttp.ClientSession() as session:
            async with session.head(url=url, allow_redirects=redirect) as response:
                return response.url, await response.text('utf-8'), response.cookies

    @classmethod
    async def options(cls, url, redirect=True) -> any:
        async with aiohttp.ClientSession() as session:
            async with session.options(url=url, allow_redirects=redirect) as response:
                return response.url, await response.text('utf-8'), response.cookies

    @classmethod
    async def patch(cls, url, data=None) -> any:
        async with aiohttp.ClientSession() as session:
            async with session.patch(url=url, data=data) as response:
                return response.url, await response.text('utf-8'), response.cookies
