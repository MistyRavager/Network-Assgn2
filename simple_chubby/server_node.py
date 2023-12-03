from server import Server
import sys
import os
import time
import threading
import socket
import json

host = 'localhost'
port = 5000

server = Server(port, host, 5)


# spawn a thread to trigger timeout every timeout_limit/2 seconds
def check_timeout():
    global server
    while True:
        server.timeout()
        time.sleep(server.timeout_limit/2)
threading.Thread(target=check_timeout).start()


'''
    client sends message in the form of a json string:
    {
        "type": "keepalive"/"request",
        "id": "id"
    }
'''
def parse_message(string):
    global server
    message = json.loads(string)
    if message['type'] == 'keepalive':
        server.handle_keepalive(message['id'])
    elif message['type'] == 'request':
        if server.handle_request(message['id']):
            print('Server granted request to', message['id'])
        else:
            print('Server denied request to', message['id'])
    else:
        print('Invalid message type')

try:
    while True:
        # listen to incoming connections using sockets
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5) # maybe make this only 1 connection at a time?
        print('Server listening....')

        # accept connection
        conn, addr = s.accept()
        print('Got connection from', addr)

        # receive data from client
        data = conn.recv(1024)
        if not data:
            break
        else:
            parse_message(data.decode('utf-8'))
        conn.close()
        s.close()

except KeyboardInterrupt:
    print('Interrupted')
    sys.exit(0)
