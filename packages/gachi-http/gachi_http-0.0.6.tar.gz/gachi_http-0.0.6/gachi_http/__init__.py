import asyncio
from aiohttp import ClientSession, ClientTimeout
from json import loads
from aiohttp_socks import ProxyConnector
from threading import Thread
from ssl import create_default_context


class Response:
    def __init__(self, status, headers, content=None):
        self.status_code = status
        self.content = content
        self.text = None
        if self.content is not None:
            self.text = self.content.decode("latin1")
        self.headers = {}
        for h in headers.keys():
            val = headers[h]
            self.headers[h] = val

    def json(self):
        return loads(self.text)

    def __repr__(self):
        return f"<Response [{self.status_code}]>"


def __startswith(word, _list):
    starts = False
    for w in _list:
        if word.startswith(w):
            starts = True
            break
    return starts


def request(method, url, params=None, data=None, json=None, headers=None, proxies=None, skip_headers=None):
    if skip_headers is None:
        skip_headers = []
    if data is None and json is None:
        skip_headers.append('Content-Type')
    if method not in ['POST', 'GET', 'PUT', 'HEAD', 'OPTIONS', 'DELETE', 'PATCH']:
        return None
    if isinstance(proxies, dict):
        proxies = list(proxies.values())[0]
        if not __startswith(proxies, ['http', 'https', 'socks4', 'socks5']):
            proxies = None
        else:
            proxies = ProxyConnector.from_url(proxies)
    return [method, url, params, data, json, headers, proxies, skip_headers]


# ---Methods---

def get(url, params=None, headers=None, proxies=None):
    return request('GET', url=url, params=params, headers=headers, proxies=proxies)


def head(url, params=None, headers=None, proxies=None):
    return request('HEAD', url=url, params=params, headers=headers, proxies=proxies)


def options(url, params=None, headers=None, proxies=None):
    return request('OPTIONS', url=url, params=params, headers=headers, proxies=proxies)


def delete(url, params=None, headers=None, proxies=None):
    return request('DELETE', url=url, params=params, headers=headers, proxies=proxies)


def post(url, params=None, data=None, json=None, headers=None, proxies=None):
    return request('POST', url=url, params=params, data=data, json=json, headers=headers, proxies=proxies)


def patch(url, params=None, data=None, json=None, headers=None, proxies=None):
    return request('PATCH', url=url, params=params, data=data, json=json, headers=headers, proxies=proxies)


def put(url, params=None, data=None, json=None, headers=None, proxies=None):
    return request('PUT', url=url, params=params, data=data, json=json, headers=headers, proxies=proxies)


async def __execReq(sess, req, ssl, include_content, exception_handler, success_handler):
    try:
        async with sess.request(method=req[0], url=req[1], params=req[2], data=req[3], json=req[4], headers=req[5],
                                proxy=req[6], skip_auto_headers=req[7], ssl=ssl) as resp:
            content = None
            if include_content:
                content = await resp.read()
            final = Response(resp.status, resp.headers, content)
            if success_handler is not None:
                Thread(target=success_handler, args=[final]).start()
            return final
    except Exception as e:
        if exception_handler is not None:
            Thread(target=exception_handler, args=[e]).start()


async def __makeReqs(reqs, size, timeout, include_content, exception_handler, success_handler):
    resp = []
    sem = asyncio.Semaphore(size)
    ssl = create_default_context()
    async with ClientSession(timeout=ClientTimeout(total=timeout)) as sess:
        async with sem:
            for req in reqs:
                data = await __execReq(sess, req, ssl, include_content, exception_handler, success_handler)
                if not data:
                    resp.append(None)
                    continue
                resp.append(data)
    return resp


def map(reqs, size=10, timeout=None, include_content=True, exception_handler=None, success_handler=None):
    if not reqs or not isinstance(reqs[0], list):
        return None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    fut = asyncio.gather(__makeReqs(reqs, size, timeout, include_content, exception_handler, success_handler))
    resp = loop.run_until_complete(fut)
    loop.close()
    return resp[0]
