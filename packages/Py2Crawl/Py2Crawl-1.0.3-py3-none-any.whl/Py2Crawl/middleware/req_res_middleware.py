from Py2Crawl.utils.request import Request
from Py2Crawl.utils.response import Response
from Py2Crawl.utils.logger import LOGGER


class ReqResMiddleware:
    def __init__(self):
        self.counter = 0

    async def process(self, request: Request):
        res = await request.execute()
        if type(res) == dict:
            self.counter = self.counter + 1
            LOGGER.info(f"Processed requests: {self.counter}")
            return await self._parse_pw_response(res)
        else:
            self.counter = self.counter + 1
            LOGGER.info(f"Processed requests: {self.counter}")
            return await self._parser_ah_response(res)

    async def _parse_pw_response(self, response: dict):
        res = Response(
            url=response.get("url"),
            content=response.get("content"),
            cookies=response.get("cookies")
        )
        return res

    async def _parser_ah_response(self, response: any):
        res = Response(
            url=response[0],
            content=response[1],
            cookies=response[2]
        )
        return res
