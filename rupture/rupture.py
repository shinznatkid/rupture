# -*- coding: utf-8 -*-
'''
    Rupture
    version 1.0.1
    build 3
'''

from bs4 import BeautifulSoup
import requests
import socket
import pickle
import ssl

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


class Rupture(object):

    timeout  = 15
    parser   = None  # None or html.parser or lxml
    encoding = None

    def __init__(self, proxies=None, parser='html.parser'):
        self.session = requests.Session()
        self.proxies = proxies
        self.parser  = parser

    def _wrap_response(self, obj):

        def get_soup(self):
            if not hasattr(self, '_soup'):
                self._soup = BeautifulSoup(self.text, self.parser, from_encoding=self.encoding)
                if self.parser == 'lxml':
                    import lxml
                    lxml.etree.clear_error_log()
            return self._soup

        def get__repr__(self):
            if hasattr(self, 'text'):
                return '<Response [%s]: %s>' % (self.status_code, self.text)
            return '<Response [%s]>' % (self.status_code)

        obj.__class__.parser = self.parser
        obj.__class__.soup = property(get_soup)
        obj.__class__.__repr__ = get__repr__
        return obj

    def http_request(self, method, url, params=None, data=None, timeout=None, proxies=None, encoding=None, **kwargs):
        timeout  = self.timeout if timeout is None else timeout
        proxies  = self.proxies if proxies is None else proxies
        encoding = self.encoding if encoding is None else encoding

        try:
            proxies = {'http': proxies, 'https': proxies} if proxies else None
            r = self.session.request(method, url, params=params, data=data, timeout=self.timeout, proxies=proxies, **kwargs)
            if encoding:
                r.encoding = encoding
            return self._wrap_response(r)
        except (ssl.SSLError, socket.error) as e:
            raise requests.exceptions.RequestException(e.message)

    def http_get(self, url, params=None, **kwargs):
        return self.http_request('GET', url, params=params, **kwargs)

    def xml_get(self, url, params=None, headers=None, **kwargs):
        xml_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json; charset=utf-8'
        }
        if headers:
            headers = dict(xml_headers.items() + headers.items())
        else:
            headers = xml_headers
        return self.http_get(url, params=params, headers=headers, **kwargs)

    def http_post(self, url, data=None, **kwargs):
        return self.http_request('POST', url, data=data, **kwargs)

    def xml_post(self, url, data=None, headers=None, **kwargs):
        xml_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json; charset=utf-8'
        }
        if headers:
            headers = dict(xml_headers.items() + headers.items())
        else:
            headers = xml_headers
        return self.http_post(url, data=data, headers=headers, **kwargs)

    def http_get_image(self, url, filepath, **kwargs):
        response = self.http_get(url, stream=True, **kwargs)
        if not response.ok:
            raise Exception('Response not okay')
        with open(filepath, 'wb') as handle:
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        return filepath

    def parse_float_or_none(self, s):
        if s:
            return float(str(s).strip().replace(',', '').replace('+', ''))
        return s

    def new_session(self):
        self.session = requests.Session()

    def serialize(self):
        return pickle.dumps([self.session])

    @classmethod
    def _deserialize_key(cls, data, keys):
        raw_results = pickle.loads(data)
        entity = cls()
        for i in range(len(keys)):
            setattr(entity, keys[i], raw_results[i])
        return entity

    @classmethod
    def deserialize(cls, data):
        return cls._deserialize_key(data, ['session'])

    def patch_ssl(self):

        class SSLAdapter(HTTPAdapter):
            def init_poolmanager(self, connections, maxsize, block=False):
                self.poolmanager = PoolManager(num_pools=connections,
                                               maxsize=maxsize,
                                               block=block,
                                               ssl_version=ssl.PROTOCOL_TLSv1)

        if not getattr(self.session, 'is_patch', False):
            self.session.is_patch = True
            self.session.mount('https://', SSLAdapter())
