import time

from flask import Flask,request,redirect,Response
import requests
from werkzeug.routing import BaseConverter
import threading
app = Flask(__name__)

config={
    'hosts':[{'host':'http://10.12.78.42:8080/','port':8080},
             {'host':'https://lcs-pandora.test.shopee.io','port':8081}
             ]
}
portMapSite={}
for host in config['hosts']:

    portMapSite[host.get('port')]= host.get('host').rstrip('/')

@app.errorhandler(404)
def proxy(args):
    path=request.path
    SITE_NAME=portMapSite.get(  int(request.host.split(':')[1]))
    if request.method=='GET':
        resp = requests.get(f'{SITE_NAME}{path}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='POST':
        resp = requests.post(f'{SITE_NAME}{path}',json=request.get_json())
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='DELETE':
        resp = requests.delete(f'{SITE_NAME}{path}').content
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response

if __name__ == '__main__':
    for host in config['hosts']:
        appSvc=threading.Thread(target=app.run,kwargs={'debug':True,'host':'0.0.0.0','port':host.get('port'),'use_reloader':False})
        appSvc.start()
    def forerver():
        while True:
            time.sleep(10000)
    forerver()


