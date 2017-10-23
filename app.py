from flask import Flask, request
import os
import socket
import json
from redis import Redis

# Connect to Redis
try:
    r = Redis(host="redis", password=os.getenv("RP", "default"), db=0, socket_connect_timeout=2, socket_timeout=2)
    cache = True
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
            try:
                a = socket.gethostbyname_ex(i)[2]
            except:
                a = ['failed']

            result[i] = a
        return json.dumps(result), 200
    else:
        return 'Forbidden', 403


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
