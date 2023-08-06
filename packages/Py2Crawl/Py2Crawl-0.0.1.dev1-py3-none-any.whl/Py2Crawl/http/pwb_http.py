from Py2Web.main import get as pw_get


class PyWebRequest:
    @classmethod
    async def get(cls, url):
        res = pw_get(url)
        return dict(res)
