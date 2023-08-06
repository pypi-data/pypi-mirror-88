import requests
import datetime as dt
from pathlib import Path
from http_api_client.io.lpickle import CachedObject


class HttpResponse():

    def __init__(self):
        self.r = None
        self.date = None

    @staticmethod
    def _parse_date(response):
        try:
            date_string = response.headers.get('Date')    
            return dt.datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
        except:
            return
    
    def add_response(self, response: requests.Response) -> bool:

        ok = False
        if isinstance(response, requests.Response):
            if response.ok:
                self.date = self._parse_date(response)
                self.r = response
                ok = True

        return ok

                
class CachedHttpResponse():

    def __init__(self, path: Path):
        self.path = path
        self.response = HttpResponse()
        self.cacher = CachedObject(path)
        self.cached = None
        self.load()

    def add(self, response):

        ok = self.response.add_response(response)
        if ok:
            self.cached = False
            self.save()

    def save(self):
        self.cacher.set(self.response)
        self.cacher.save()

    def load(self):
        
        response = self.cacher.load()

        if isinstance(response, HttpResponse):
            self.response = response
            self.cached = True
