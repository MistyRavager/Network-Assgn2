from server import Server
import sys
# import os
import time
import threading
import socket
import json

# host = '127.0.0.1'
host = '10.0.0.1'
port = 5000

server = Server(port, host, 5)


# spawn a thread to trigger timeout every timeout_limit/2 seconds
def check_timeout():
    global server
    while True:
        for i in range(server.num_locks):
            server.timeout(i)
        time.sleep(server.timeout_limit/2)


threading.Thread(target=check_timeout).start()


def parse_message(string: str) -> str:
    '''
        returns a json string to send back to the client

        server sends message in the form of a json string:
        {
            "type": "keepalive"/"request",
            "lock_num": int,
            "value": "ack"/"nak"
        }
        This parses the message and calls the appropriate server method
    '''
    global server
    message = json.loads(string)
    if message['type'] == 'keepalive':
        if server.handle_keepalive(message['id'], message['lock_num']):
            print(f"Server received keepalive from {message['id']} for lock {message['lock_num']}")
            return make_message('keepalive', 'ack', message['lock_num'])
        else:
            print(f"Server received invalid keepalive from {message['id']} for lock {message['lock_num']}")
            return make_message('keepalive', 'nak', message['lock_num'])
    elif message['type'] == 'request':
        if server.handle_request(message['id'], message['lock_num']):
            print(f"Server granted request to {message['id']} for lock {message['lock_num']}")
            return make_message('request', 'ack', message['lock_num'])
        else:
            print(f"Server denied request to {message['id']} for lock {message['lock_num']}")
            return make_message('request', 'nak', message['lock_num'])
    else:
        print('Invalid message type')
    return None


def make_message(type: str, value: str, lock_num: int) -> str:
    '''
        make_message() creates a json string to send back to the client

        server sends message in the form of a json string:
        {
            "type": "keepalive"/"request",
            "lock_num": int,
            "value": "ack"/"nak"
        }
    '''
    message = {
        'type': type,
        'lock_num': lock_num,
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
