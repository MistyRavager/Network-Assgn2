from server import Server
import sys
# import os
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


def parse_message(string: str) -> str:
    '''
        returns a json string to send back to the client

        server sends message in the form of a json string:
        {
            "type": "keepalive"/"request",
            "value": "ack"/"nak"
        }
        This parses the message and calls the appropriate server method
    '''
    global server
    message = json.loads(string)
    if message['type'] == 'keepalive':
        if server.handle_keepalive(message['id']):
            print('Server received keepalive from', message['id'])
            return make_message('keepalive', 'ack')
        else:
            print('Server received invalid keepalive from', message['id'])
            return make_message('keepalive', 'nak')
    elif message['type'] == 'request':
        if server.handle_request(message['id']):
            print('Server granted request to', message['id'])
            return make_message('request', 'ack')
        else:
            print('Server denied request to', message['id'])
            return make_message('request', 'nak')
    else:
        print('Invalid message type')
    return None


def make_message(type: str, value: str) -> str:
    '''
        make_message() creates a json string to send back to the client

        server sends message in the form of a json string:
        {
            "type": "keepalive"/"request",
            "value": "ack"/"nak"
        }
    '''
    message = {
        'type': type,
        'value': value
    }
    return json.dumps(message)


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print('Server ready....')
    
    while True:
        data, addr = s.recvfrom(1024)
        print('Server received message from', addr)
        response = parse_message(data.decode('utf-8'))
        if response:
            s.sendto(response.encode('utf-8'), addr)

except KeyboardInterrupt:
    s.close()
    print('Interrupted')
    sys.exit(1)
