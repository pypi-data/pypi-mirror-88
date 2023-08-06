from Py2Crawl.middleware.req_res_middleware import ReqResMiddleware
from Py2Crawl.utils.request import Request
from Py2Crawl.utils.response import Response
from Py2Crawl.http.methods import PyCrawlMethods
from PySide2.QtWidgets import QApplication


class PyCrawlSpider:
    def __init__(self, start_urls: list, start_urls_method: PyCrawlMethods, callback):
        self.start_urls: list = start_urls
        self.callback = callback
        self.start_urls_method = start_urls_method
        self.crawled = []
        self.req_res = ReqResMiddleware()
        self.q_app = QApplication([])

    async def execute(self, request: Request):
        if str(request.url) in self.crawled:
            return
        res: Response = await self.req_res.process(request)
        self.crawled.append(str(res.url))
        await self._from_crawler(res)

    async def _from_crawler(self, response: Response):
        await self.callback(response)

    async def start_crawler(self):
        for i in self.start_urls:
            r = Request(
                url=i,
                method=self.start_urls_method
            )
            await self.execute(r)
