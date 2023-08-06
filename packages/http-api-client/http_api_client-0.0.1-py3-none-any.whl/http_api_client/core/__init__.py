import requests
from urllib.parse import urlparse, ParseResult, urljoin
from pathlib import Path
import datetime as dt
import logging
from pprint import pformat
from http_api_client import placeholder_logger
from .responses import HttpResponse, CachedHttpResponse


class HttpClient():
    """
    Helper class for REST Apis, with inbuilt cacher(for GET)

    :param root_url: API root url
    :type root_url: str or urllib.parse.ParseResult
    :param auth: authentication
    :type auth: dict
    :param verify_ssl: verify ssl 
    :type verify_ssl: bool
    :param timeout: default timeout
    :type timeout: float
    :param cache_dir: directory where cache files are stored for GET requests
    :type cache_dir: pathlib.Path
    :param api_id: api_id for caching
    :type api_id: str
    :param log: logger
    :type log: logging.Logger
    """

    def __init__(self, root_url, auth: dict = {}, verify_ssl=False, timeout=10,
                 cache_dir: Path = Path('.'),
                 api_id: str = '', log: logging.Logger = None):

        self.root_url = root_url if isinstance(root_url, ParseResult) else urlparse(root_url)
        self.log = log if isinstance(log, logging.Logger) else placeholder_logger()
        self.auth = auth
        self.api_id = api_id
        self.cache_dir = cache_dir

        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
        self.hostname = self.root_url.hostname
        self.port = self.root_url.port
        
        self.api = {
            'GET': {},
            'POST': {},
            'PACTH': {},
        }

    def add(self, _id, url, method):

        tgt = self.api.get(method)

        if not isinstance(tgt, dict):
            return

        tgt[_id] = url
                      
    def parse_api(self, api):        
        """
        Parse an API dictionary with following structure

        .. code-block:: python

            api = {
                'path': {'path': 'url', 'methods': ['GET', 'POST', 'PATCH']},
            }

        """
        for _id, conf in api.items():
            
            path = conf.get('path')        
            url = urljoin(self.root_url.geturl(), path)

            methods = conf.get('methods')
            
            for method in methods:
                self.add(_id, url, method)
        
    def _get(self, url, params: dict = {}, **kwargs) -> requests.Response:
        """
        Get using requests, class internal method
        """        
        try:
            return requests.get(url, params, **kwargs)

        except Exception as e:
            self.log.info(f'Error GET from {url}: {e!r}')

    def _post(self, url, data: dict = {}, json: dict = {}, **kwargs) -> requests.Response:
        """
        Post using requests, class internal method
        """

        try:
            if data:
                self.log.debug(pformat(data))

            if json:
                self.log.debug(pformat(json))

        except:
            pass
        
        try:
            return requests.post(url, data=data, json=json, **kwargs)

        except Exception as e:
            self.log.info(f'Error POST from {url}: {e!r}')

    def _patch(self, url, data: dict = {}, **kwargs) -> requests.Response:
        """
        Patch using requests, class internal method
        """
        try:
            if data:
                self.log.debug(pformat(data))
        
        except:
            pass

        try:
            return requests.patch(url, data=data, **kwargs)

        except Exception as e:
            self.log.info(f'Error PATCH from {url}: {e!r}')
            
    def get(self, name: str, params: dict = {}, use_cache: dt.timedelta = dt.timedelta(0), **kwargs) -> CachedHttpResponse:
        """
        Send a GET request

        :param name: name for path in GET paths        
        :type name: str
        :param params: parameters for GET request
        :type params: dict
        :param use_cache: Specify if cache should be used
        :type use_cache: datetime.timedelta
        
        :returns: Response for request, possible cached
        :rtype: CachedHttpResponse
        """        
        url = self.api['GET'].get(name)

        path = self.cache_dir / f'{self.api_id}_get_{name}.pickle'
        response = CachedHttpResponse(path)

        if use_cache > dt.timedelta(0) and response.cached:

            now = dt.datetime.utcnow()
            date = response.response.date
            age = now - date
            
            if date + use_cache > now:
                
                self.log.info(f'Using cached response, age: {age}')
                return response

            self.log.info(f'Updating cache, age: {age}')
                
        response.add(self._get(url, params, **kwargs))
                        
        return response

    def post(self, name: str, data: dict = {}, json: dict = {}, **kwargs) -> HttpResponse:
        """
        Send a POST request
        """
        url = self.api['POST'].get(name)

        response = HttpResponse()
        
        response.add_response(self._post(url, data, json, **kwargs))

        return response
        
    def patch(self, name: str, data: dict = {}, **kwargs) -> HttpResponse:
        """
        Send a PATCH request
        """
        url = self.api['PATCH'].get(name)        
        return HttpResponse().add_response(self._patch(url, data, **kwargs))



        
        

