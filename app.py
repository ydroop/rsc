from flask import Flask, request
import os
import socket
import json
from redis import Redis
from datetime import timedelta
from random import timedelta

# Connect to Redis
try:
    r = Redis(host="redis", password=os.getenv("RP", "default"), db=0, socket_connect_timeout=2, socket_timeout=2)
    cache = True
    print "cache ok"
except:
    cache = False
    print "no cache"

app = Flask(__name__)

@app.route("/")
def hello():
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

@app.route("/bns/", methods=['POST'] )
def bns():
    if request.is_json:
        ns_list = request.get_json()
        result = {}
        for i in ns_list:
            if cache and r.exists(i):
                a = json.loads( r.get(i) )
            else:
                try:
                    a = socket.gethostbyname_ex(i)[2]
                except:
                    a = ['failed']
                if cache:
                    print 'update cache for '+ str(i)
                    r.set( i, json.dumps( a ) )
                    r.expire( i , timedelta(days=randint(2,5) )
            result[i] = a
        return json.dumps(result), 200
    else:
        return 'Forbidden', 403

@app.route("/status/", methods=['POST'] )
def status():
    if request.is_json:
        ns_list = request.get_json()
        if cache:
            c_list = r.keys()
        else:
            c_list = []
                             
        in_cache = len( c_list )
        result = len(set(ns_list) - set(c_list) )
        request_len = len( ns_list ) 
                             
        return json.dumps( { 'total_cached' : in_cache, 'cached_in_request' : result , 'in_request' : request_len } ), 200
    else:
        return 'Forbidden', 403                            
        
        

                             
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
