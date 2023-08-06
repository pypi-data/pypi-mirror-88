from Py2Crawl.exceptions import InvalidUrl


def valid_url(url: str):
    if not "://" in url:
        raise InvalidUrl(url)
    else:
        return url
