from Py2Web.main import get as pw_get


class Py2WebRequest:
    @classmethod
    async def get(cls, url):
        res = pw_get(url)
        return dict(res)
