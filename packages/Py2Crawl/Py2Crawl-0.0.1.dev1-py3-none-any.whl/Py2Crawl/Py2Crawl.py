from Py2Crawl.utils.logging import init_logger
from Py2Crawl.settings.base_settings import BaseSettings
from Py2Crawl.utils.sentry import init_sentry
from Py2Crawl.exceptions import SentryDSNNotSet
from Py2Crawl.spider import PyCrawlSpider


class Py2Crawl:
    def __int__(self, settings=BaseSettings()):
        self.settings = settings
        self.logger = init_logger()

        if self.settings.SENTRY:
            if not self.settings.SENTRY_DSN == type(str):
                raise SentryDSNNotSet
            init_sentry(str(self.settings.SENTRY_DSN))

    async def crawl(self, spider: PyCrawlSpider, *args, **kwargs):
        await spider.start_crawler()
