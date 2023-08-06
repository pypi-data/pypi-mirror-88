# A simple wrapper of requests, easy but useful!

## Installation
```bash
pip install webrequests
```

## Features
- Random User-Agent automatic
- Try again when request failed
- Download file from an URL
- Get a soup from an URL

## Usage
```python
from webrequests import WebRequest


url = 'http://output.nsfc.gov.cn/captcha/defaultCaptcha'

# request an url
resp = WebRequest.get_response(url)
resp = WebRequest.get_response(url, method='POST', max_try=5, timeout=5)
print(resp.headers)


# download file from an url
WebRequest.download(url, 'out.jpg')
WebRequest.download(url, 'out.jpg', max_try=5, timeout=10)


# request with session
import requests

session = requests.session()
resp = WebRequest.get_response(url, session=session)
print(resp.cookies)
print(session.cookies)


# get a soup
url = 'http://www.cip.cc/'
soup = WebRequest.get_soup(url)
print(soup.select_one('.kq-well pre').text.strip())
```
