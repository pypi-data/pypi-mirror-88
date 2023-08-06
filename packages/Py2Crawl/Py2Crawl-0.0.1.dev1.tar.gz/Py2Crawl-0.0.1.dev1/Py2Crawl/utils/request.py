from Py2Crawl.http.methods import PyCrawlMethods
from Py2Crawl.http.pwb_http import PyWebRequest
from Py2Crawl.http.a_http import AsyncHttpRequest
from Py2Crawl.exceptions import InvalidMethod
from Py2Crawl.utils.input_validation import valid_url


class Request:
    def __init__(self, url: str, method: PyCrawlMethods, params: dict = None, data: dict = None, json: dict = None, redirect: bool = True):
        self.url = valid_url(url)
        self.method = method
        self.redirect = redirect
        self.params = params
        self.data = data
        self.json = json

    async def execute(self):
        if self.method == PyCrawlMethods.PW_GET:
            return await PyWebRequest().get(self.url)
        elif self.method == PyCrawlMethods.AH_GET:
            return await AsyncHttpRequest().get(url=self.url, redirect=self.redirect, params=self.params)
        elif self.method == PyCrawlMethods.AH_POST:
            return await AsyncHttpRequest().post(url=self.url, data=self.data, json=self.json)
        elif self.method == PyCrawlMethods.AH_PUT:
            return await AsyncHttpRequest().put(url=self.url, data=self.data)
        elif self.method == PyCrawlMethods.AH_DELETE:
            return await AsyncHttpRequest().delete(url=self.url)
        elif self.method == PyCrawlMethods.AH_HEAD:
            return await AsyncHttpRequest().head(url=self.url, redirect=self.redirect)
        elif self.method == PyCrawlMethods.AH_OPTIONS:
            return await AsyncHttpRequest().options(url=self.url, redirect=self.redirect)
        elif self.method == PyCrawlMethods.AH_PATCH:
            return await AsyncHttpRequest().patch(url=self.url, data=self.data)
        else:
            raise InvalidMethod(self.method)
