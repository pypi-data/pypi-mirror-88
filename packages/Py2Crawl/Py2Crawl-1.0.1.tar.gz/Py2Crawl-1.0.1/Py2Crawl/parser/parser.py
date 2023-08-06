from lxml import html
from urllib.parse import urlparse
from Py2Crawl.settings.parser_settings import ParserSettings


class HTMLParser:
    def __init__(self, content: str, encoding='utf-8'):
        self.content = html.fromstring(html=content)
        self.encoding = encoding

    async def get_lxml_obj(self):
        return self.content

    async def get_all_links(self):
        links: list = []
        for i in ParserSettings.xpath_urls:
            for j in self.content.xpath(str(i)):
                links.append(j)
        return links if len(links) > 0 else None

    async def get_all_third_party_links(self, base_url: str):
        b_url: urlparse = urlparse(base_url)
        links: list = []
        for i in ParserSettings.xpath_urls:
            for j in self.content.xpath(str(i)):
                if urlparse(j).netloc != b_url.netloc and urlparse(j).netloc != "":
                    links.append(j)
        return links if len(links) > 0 else None

    async def get_all_links_from_scope(self, base_url: str):
        b_url: urlparse = urlparse(base_url)
        links: list = []
        for i in ParserSettings.xpath_urls:
            for j in self.content.xpath(str(i)):
                if urlparse(j).netloc == b_url.netloc or urlparse(j).netloc == "":
                    if urlparse(j).netloc == "" and not str(j).startswith("/"):
                        continue
                    links.append(j)
        return links if len(links) > 0 else None

    async def get_all_headlines(self):
        headlines: list = []
        for i in ParserSettings.xpath_headlines:
            for j in self.content.xpath(i):
                headlines.append(j)
        return headlines if len(headlines) > 0 else None
