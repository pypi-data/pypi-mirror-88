from Py2Crawl.Py2Crawl import Py2Crawl
from Py2Crawl.spider import PyCrawlSpider
from Py2Crawl.http.methods import PyCrawlMethods
from Py2Crawl.parser.parser import HTMLParser
from Py2Crawl.utils.request import Request
from urllib.parse import urlparse
import asyncio


async def main():
    async def test_func(response):
        parser = HTMLParser(response.content)
        c = await parser.get_lxml_obj()
        print(c.xpath("//h4/text()"))
        print('\n')
        print(response.url)
        print(response.cookies)
        l = await parser.get_all_links_from_scope(str(response.url))
        to_scrape = []
        for i in l:
            if not i or not len(i) > 0:
                continue
            if str(i).startswith("#"):
                continue
            to_scrape.append(f"https://{urlparse(str(response.url)).netloc}{str(i)}")
        for i in to_scrape:
            r = Request(
                url=str(i),
                method=PyCrawlMethods.PW_GET
            )
            await spider.execute(r)

    crawler = Py2Crawl()
    spider = PyCrawlSpider(
        start_urls=["https://secjur.com/"],
        start_urls_method=PyCrawlMethods.PW_GET,
        callback=test_func
    )
    await crawler.crawl(spider)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except RuntimeError as e:
        print("Loop closed!!")
    finally:
        loop.close()
