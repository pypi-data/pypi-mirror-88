class SentryDSNNotSet(Exception):
    def __init__(self):
        super().__init__("Sentry DSN not set.")


class InvalidMethod(Exception):
    def __init__(self, meth):
        super().__init__(f"Method {meth} is not valid. Use a method form PyCrawl.http.methods.PyCrawlMethods")


class InvalidUrl(Exception):
    def __init__(self, url):
        super().__init__(f"URL: {url} is not valid.")
