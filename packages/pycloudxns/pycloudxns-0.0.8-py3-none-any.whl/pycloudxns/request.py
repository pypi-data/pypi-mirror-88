# -*- coding: utf-8 -*-

import requests
import logging
import hashlib
import functools
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError
import time

logger = logging.getLogger(__name__)


def retry(loop=3,delay=1):
    def trace(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1,loop+1):
                logger.debug(f'第{i}次請求 {args} {kwargs}')
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    logger.warning(f'重試第{i}次 {e} {args} {kwargs}')
                    time.sleep(delay)

        return wrapper

    return trace


class HTTP:
    headers = {
        'Content-Type': 'application/json',
        'user-agent': 'CloudXNS-Python/v3',
        'API-KEY': "",
        'API-REQUEST-DATE': "",
        'API-HMAC': "",
        'API-FORMAT': 'json',
    }
    API_URL = "https://www.cloudxns.net/api2"

    def __init__(self, API_KEY, SECRET_KEY):
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY

    def set_api_key(self, key):
        self.headers['API-KEY'] = key

    def set_date(self, date):
        self.headers['API-REQUEST-DATE'] = date

    def set_hmac(self, hmac):
        self.headers['API-HMAC'] = hmac

    @retry()
    def request(self, method, uri, **kwargs) -> dict:
        url = f"{self.API_URL}/{uri}"
        logging.debug(url)
        data = kwargs.get('data', '')

        REQUEST_DATE = time.strftime('%a %b %d %H:%M:%S %Y', time.localtime())
        sign_raw = (
            self.API_KEY,
            "%s%s" % (url, "?%s" % str("&".join([f"{k}={v}" for k, v in kwargs['params'].items()])) if kwargs.get('params') else ""),
            data,
            REQUEST_DATE,
            self.SECRET_KEY
        )
        sign = "".join(sign_raw)
        API_HMAC = hashlib.md5(sign.encode()).hexdigest()
        self.set_api_key(self.API_KEY)
        self.set_hmac(API_HMAC)
        self.set_date(REQUEST_DATE)

        try:
            req = requests.api.request(method=method, url=url, timeout=600, headers=self.headers, **kwargs)

            if req.status_code == 400:
                raise ConnectionError(f'400 超時 {url}')
            elif req.status_code != 200:
                return {'code': req.status_code, 'message': f'Response {req.status_code} {url}'}
            else:
                return req.json()

        except JSONDecodeError:
            logger.error(f'獲取json出錯')
            return {'code': 1, 'message': f'獲取json出錯'}
        except ConnectionError:
            raise ConnectionError(f'連接超時 {url}')
        except Exception as e:
            logger.error(f'未知錯誤 {e} {type(e)}')
            return {'code': 1, 'message': f'未知錯誤 {e} {type(e)}'}

    def get(self, url, params=None, **kwargs) -> dict:
        r"""Sends a GET request.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('get', url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs) -> dict:
        r"""Sends a POST request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('post', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs) -> dict:
        r"""Sends a PUT request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('put', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('delete', url, **kwargs)
