import threading
import time

import requests
from flask import Flask, request, Response

app = Flask(__name__)

config = {
    'hosts': [{'host': 'http://10.12.78.42:8080/', 'port': 8080},
              {'host': 'https://lcs-pandora.test.shopee.io', 'port': 8081}
              ]
}
portMapSite = {}
for host in config['hosts']:
    portMapSite[host.get('port')] = host.get('host').rstrip('/')


@app.errorhandler(404)
def proxy(args):
    path = request.path
    SITE_NAME = portMapSite.get(int(request.host.split(':')[1]))
    if request.method == 'GET':
        query_string=request.query_string.decode('utf-8','ignore')
        resp = requests.get(f'{SITE_NAME}{path}?{query_string}',)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method == 'POST':
        resp = requests.post(f'{SITE_NAME}{path}', json=request.get_json())
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    else:
        method=request.method.lower()
        if hasattr(requests,method):
            resp=getattr(requests,method)(f'{SITE_NAME}{path}').content
            excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
            headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
            response = Response(resp.content, resp.status_code, headers)
            return response
        else:
            print('not support')



if __name__ == '__main__':
    for host in config['hosts']:
        appSvc = threading.Thread(target=app.run, kwargs={'debug': True, 'host': '0.0.0.0', 'port': host.get('port'),
                                                          'use_reloader': False})
        appSvc.start()


    def forerver():
        while True:
            time.sleep(10000)


    forerver()
