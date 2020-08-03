from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, HTTPError
import logging


class HttpRequests:
    def __init__(self, base_url, api_key):
        self.url = base_url
        self.header = {"user-key": api_key}

    def get_details(self, api_name, query_param=None):
        session = Session()
        Zomato_adapter = HTTPAdapter(max_retries=3)
        session.mount(self.url+api_name, Zomato_adapter)
        if query_param:
            try:
                return session.get(headers=self.header, url=self.url + api_name, params=query_param, timeout=(2, 5))
            except ConnectionError as ce:
                logging.error(ce)
            except HTTPError as he:
                logging.error(he)
        else:
            try:
                return session.get(headers=self.header, url=self.url + api_name, timeout=(2, 5))
            except ConnectionError as ce:
                logging.error(ce)
            except HTTPError as he:
                logging.error(he)
