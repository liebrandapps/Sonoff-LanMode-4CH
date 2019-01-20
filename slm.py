import json
import select
import sys
import threading
import time
from websocket import create_connection


class SonOffControl:

    def __init__(self, ws):
        self.ws = ws
        self.deviceId = 'nonce'
        self.apikey = 'nonce'
        self.terminate = False

    def initMsg(self):
        return json.dumps({
            'action': "userOnline",
            'ts' : int(time.time()),
            'version' : 6,
            'apikey': 'nonce',
            'sequence': str(time.time()).replace('.',''),
            'userAgent': 'app'
        })

    def updateMessage(self, outlet, state):
        return json.dumps({
            'action' : 'update',
            'device' : self.deviceId,
            'apiKey': self.apikey,
            'selfApikey': 'nonce',
            'params' : {'switches': [ {'switch' : state, 'outlet': outlet } ] },
            'sequence': str(time.time()).replace('.',''),
            'userAgent': 'app'
        })

    def receiver(self):
        print("Starting Receiver")
        try:
            while True:
                sock = [self.ws.sock,]
                ready = select.select(sock, [],[])
                if len(ready[0])>0 and ready[0][0]==self.ws.sock:
                    result = self.ws.recv()
                    print("Received '%s'" % result)
                    dct = json.loads(result)
                    if 'deviceId' in dct and dct['deviceid']!='nonce':
                        self.deviceId = dct['deviceid']
                    if 'apikey' in dct and dct['apikey']!='nonce':
                        self.apikey = dct['apikey']
        except:
            pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]
    else:
        print("Provide IP of your 4CH sonoff switch device as parameter")
        sys.exit(-1)
    ws = create_connection("ws://%s:8081" % addr)
    o = SonOffControl(ws)
    t = threading.Thread(target=o.receiver)
    t.daemon = True
    t.start()
    print ("mm")
    dta = o.initMsg()
    ws.send(dta)
    print ("Sent: " + dta)
    time.sleep(2)

    dta = o.updateMessage(0, 'on')
    ws.send(dta)
    print ("Sent: " + dta)
    time.sleep(1)
    dta = o.initMsg()
    ws.send(dta)
    time.sleep(4)

    dta = o.updateMessage(0, 'off')
    ws.send(dta)
    print ("Sent: " + dta)
    time.sleep(1)
    dta = o.initMsg()
    ws.send(dta)
    time.sleep(5)
    ws.close()
