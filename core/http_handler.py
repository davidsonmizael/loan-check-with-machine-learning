import requests
import json

def get_request( url, headers=None, parameters=None, return_json=True):
    result = {}
    result['status_code'] = -1
    try:
        r = requests.get(url,headers=headers, params=parameters)
        result['status_code'] = r.status_code

        if r.status_code >= 200 and r.status_code <= 202:
            if return_json:
                result['content'] = r.json()
            else:
                result['content'] = r.content
        else:
            result['content'] = r.content
    except:
        raise Exception(f'Failed to run get request to {url}')

    return result

def post_request(url, headers=None, data=None, return_json=True):
    result = {}
    result['status_code'] = -1
    try:
        r = requests.post(url, headers=headers, data=json.dumps(data))
        result['status_code'] = r.status_code

        if r.status_code >= 200 and r.status_code <= 202:
            if return_json:
                result['content'] = r.json()
            else:
                result['content'] = r.content
        else:
            result['content'] = r.content

    except:
        raise Exception(f'Failed to run get request to {url}')

    return result