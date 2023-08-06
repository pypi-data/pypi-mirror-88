class Response:
    def __init__(self, url: str, content: str, cookies: dict = None):
        self.url = url
        self.content = content
        self.cookies = cookies
