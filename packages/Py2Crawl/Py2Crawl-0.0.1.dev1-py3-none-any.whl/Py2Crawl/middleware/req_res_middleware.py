from Py2Crawl.utils.request import Request
from Py2Crawl.utils.response import Response


class ReqResMiddleware:
    def __init__(self):
        self.counter = 0

    async def process(self, request: Request):
        res = await request.execute()
        if type(res) == dict:
            return await self._parse_pw_response(res)
        else:
            return await self._parser_ah_response(res)

    async def _parse_pw_response(self, response: dict):
        res = Response(
            url=response.get("url"),
            content=response.get("content"),
            cookies=response.get("cookies")
        )
        self.counter = self.counter + 1
        return res

    async def _parser_ah_response(self, response: any):
        res = Response(
            url=response[0],
            content=response[1],
            cookies=response[2]
        )
        self.counter = self.counter + 1
        return res
