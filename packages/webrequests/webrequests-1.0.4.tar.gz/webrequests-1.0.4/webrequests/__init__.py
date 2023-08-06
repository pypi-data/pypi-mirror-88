# -*- coding=utf-8 -*-
import os
import time
import json
import random

import bs4
import requests

from simple_loggers import SimpleLogger


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

version_info = json.load(open(os.path.join(BASE_DIR, 'version.json')))

__version__ = version_info['version']

class WebRequest(object):
    """
    >>> url = 'http://output.nsfc.gov.cn/captcha/defaultCaptcha'

    >>> resp = WebRequest.get_response(url)
    >>> if resp:
    >>>     print(type(resp))
    >>>     print(resp.headers)
    >>> else:
    >>>     print('failed')
    
    >>> WebRequest.download(url, 'out.jpg')

    >>> session = requests.session()
    >>> resp = WebRequest.get_response(url, session=session)
    >>> print(resp.cookies)
    >>> print(session.cookies)

    >>> url = 'http://www.cip.cc/'
    >>> soup = WebRequest.get_soup(url)
    >>> print(soup.select_one('.kq-well pre').text.strip())
    """
    logger = SimpleLogger(name='WebRequest', level='info')

    @classmethod
    def random_ua(cls):
        ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
        return {'User-Agent': random.choice(ua_list)}


    @classmethod
    def get_response(cls, url, method='GET', session=None, max_try=10, allowed_codes=[200], **kwargs):
        """
            params
                - allowed_codes: the status_code

            Return a response object
        """
        if 'headers' not in kwargs:
            kwargs['headers'] = cls.random_ua()
        elif 'User-Agent' not in kwargs['headers']:
            kwargs['headers'].update(cls.random_ua())

        for n in range(max_try):
            try:
                r = session or requests
                resp = r.request(method, url, **kwargs)
                if resp.status_code in allowed_codes:
                    return resp
                cls.logger.warning('{}st time bad status code: {} [{}]'.format(n + 1, resp.status_code, resp.text))
            except Exception as e:
                cls.logger.debug('{}st time failed for url: {}, as {}'.format(n + 1, url, e))
            time.sleep(random.randint(2, 6))
        
        cls.logger.error('failed requests for url: {}'.format(url))
        exit(1)
        
    @classmethod
    def download(cls, url, outfile, chunk_size=1024, **kwargs):
        """
            Download file from an url
        """
        resp = cls.get_response(url, stream=True, **kwargs)
        with open(outfile, 'wb') as out:
            for chunk in resp.iter_content(chunk_size):
                out.write(chunk)
        cls.logger.info('save file: {}'.format(outfile))

    @classmethod
    def get_soup(cls, url, features='html.parser', **kwargs):
        """
            features: html.parser, lxml

            Return: a BeautifulSoup object
        """
        resp = cls.get_response(url, **kwargs)
        soup = bs4.BeautifulSoup(resp.text, features=features)
        return soup


if __name__ == '__main__':

    url = 'http://output.nsfc.gov.cn/captcha/defaultCaptcha'

    resp = WebRequest.get_response(url)
    if resp:
        print(type(resp))
        print(resp.headers)
    else:
        print('failed')
    
    WebRequest.download(url, 'out.jpg')

    session = requests.session()
    resp = WebRequest.get_response(url, session=session)
    print(resp.cookies)
    print(session.cookies)

    url = 'http://www.cip.cc/'
    soup = WebRequest.get_soup(url)
    print(soup.select_one('.kq-well pre').text.strip())