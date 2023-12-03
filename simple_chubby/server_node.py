from server import Server
import sys
import os
import time
import threading

host = 'localhost'
port = 5000

server = Server(port, host, 5)

def check_timeout():
    global server
    while True:
        server.timeout()
        time.sleep(server.timeout_limit/2)

threading.Thread(target=check_timeout).start()

try:
    while True:
        # get message from a requestor
        msg = []

except KeyboardInterrupt:
    print('Interrupted')
    sys.exit(0)