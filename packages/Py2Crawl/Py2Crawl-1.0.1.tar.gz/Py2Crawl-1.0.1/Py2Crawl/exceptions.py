class SentryDSNNotSet(Exception):
    def __init__(self):
        super().__init__("Sentry DSN not set.")


class CanNotImportSentry(Exception):
    def __init__(self):
        super().__init__("There is no package sentry_sdk. Please run 'pip install sentry_sdk' or set SENTRY in "
                         "BaseSettings to False.")


class InvalidMethod(Exception):
    def __init__(self, meth):
        super().__init__(f"Method {meth} is not valid. Use a method form PyCrawl.http.methods.PyCrawlMethods")


class InvalidUrl(Exception):
    def __init__(self, url):
        super().__init__(f"URL: {url} is not valid.")
