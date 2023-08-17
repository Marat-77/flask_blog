# import os

import requests
from werkzeug.exceptions import NotFound

from flask_front.config import API_HOST, API_PORT, API_TIMEOUT

# API_PORT = '5050'
# api_port = '5050'
# API_HOST = 'http://127.0.0.1'
# api_host = 'http://127.0.0.1'
# API_TIMEOUT = 10

# API_HOST = os.getenv('API_HOST')
# API_PORT = os.getenv('API_PORT')
# API_TIMEOUT = int(os.getenv('API_TIMEOUT'))
# api_host_port = f'http://{API_HOST}:{API_PORT}'
api_hostname = API_HOST if (
        API_HOST.startswith('https://') or API_HOST.startswith('http://')
) else f'http://{API_HOST}'
api_host_port = f'{api_hostname}:{API_PORT}'


def get_from_api(api_path, headers_=None):
    # api_url = f'{API_HOST}:{API_PORT}{api_path}'
    api_url = f'{api_host_port}{api_path}'
    with open('mylog.txt', 'a', encoding='utf-8') as mlog:
        mlog.write(f'{api_url}\n')
    if headers_:
        try:
            return requests.get(api_url, timeout=API_TIMEOUT, headers=headers_)
        except Exception as err:
            print('get_from_api error:', err)
            raise NotFound
    try:
        if api_path == '/api/':
            rrr = requests.get(api_url, timeout=API_TIMEOUT)
            return rrr, api_url
        return requests.get(api_url, timeout=API_TIMEOUT)
    except Exception as err:
        print('get_from_api error:', err)
        raise NotFound


def post_to_api(api_path, to_api_payload, headers_=None):
    print('\n !!! post_to_api !!!')
    # api_url = f'{API_HOST}:{API_PORT}{api_path}'
    api_url = f'{api_host_port}{api_path}'
    if headers_ is None:
        try:
            api_request_ = requests.post(api_url,
                                         json=to_api_payload,
                                         timeout=API_TIMEOUT)
        except Exception as err:
            print('post_to_api error:', err)
            raise NotFound
        else:
            return api_request_
    headers_['Content-Type'] = 'application/json'
    try:
        api_request_ = requests.post(api_url,
                                     json=to_api_payload,
                                     headers=headers_,
                                     timeout=API_TIMEOUT)
    except Exception as err:
        print('post_to_api error:', err)
        raise NotFound
    else:
        return api_request_
