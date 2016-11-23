import json
from http.client import HTTPMessage, parse_headers
from tornado.httputil import HTTPHeaders


class MockResponse:
    def __init__(self, json_data=None, status_code=None, url=None,
                 encoding=None, _content=None, headers=HTTPHeaders({}),
                 history=None, reason=None, cookies=None, elapsed=None,
                 request=None, ok=False):
        self.ok = ok
        self.headers = headers
        self.history = history
        self.reason = reason
        self.cookies = cookies
        self.elapsed = elapsed
        self.request = request
        self._content = _content
        self.url = url
        self.encoding = encoding if encoding else 'utf-8'
        self.json_data = json_data
        self.status_code = status_code
        self.text = _content.decode(self.encoding)

        # httplib response compatability:
        self.status = status_code
        self.msg = HTTPMessage()
        self.version = 1
        self.reason = None
        self.strict = 0
        self.original_response = self
        self.closed = False

    def json(self):
        return self.json_data if self.json_data else json.loads(self.text)

    def get_json(self):
        return self.json()

    def url(self):
        return self.url

    def encoding(self):
        return self.encoding

    def status_code(self):
        return self.status_code

    def _content(self):
        return self._content

    def headers(self):
        return self.headers

    def history(self):
        return self.history

    def reason(self):
        return self.reason

    def cookies(self):
        return self.cookies

    def elapsed(self):
        return self.elapsed

    def request(self):
        return self.request

    def ok(self):
        return self.ok

    def info(self):
        return self.headers

    def isclosed(self):
        return self.closed

    def close(self):
        self.closed = True
