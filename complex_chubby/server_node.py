from server import Server
import sys
# import os
import time
import threading
import socket
import json
from dir import *
from Complex.replica import Replica
from Complex.acceptor import Acceptor
from Complex.leader import Leader
# later problem.

# host = '127.0.0.1'
id = int(sys.argv[1])
ipp = chubbies[id]

server = Server(ipp[0], ipp[1], 5)
replica = Replica(int(sys.argv[1]))
leader = Leader(int(sys.argv[1]))
acceptor = Acceptor(int(sys.argv[1]))


# spawn a thread to trigger timeout every timeout_limit/2 seconds
def check_timeout():
    global server
    while True:
        for i in range(server.num_locks):
            server.timeout(i)
        time.sleep(server.timeout_limit/2)


threading.Thread(target=check_timeout).start()


def handle(string: str) -> str:
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
            # print(f"Server received keepalive from {message['id']} for lock {message['lock_num']}")
            return make_message('keepalive', 'ack', message['lock_num'])
        else:
            # print(f"Server received invalid keepalive from {message['id']} for lock {message['lock_num']}")
            return make_message('keepalive', 'nak', message['lock_num'])
    elif message['type'] == 'request':
        if server.handle_request(message['id'], message['lock_num']):
            # print(f"Server granted request to {message['id']} for lock {message['lock_num']}")
            return make_message('request', 'ack', message['lock_num'])
        else:
            # print(f"Server denied request to {message['id']} for lock {message['lock_num']}")
            return make_message('request', 'nak', message['lock_num'])
    # else:
    #     print('Invalid message type')
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
    s.bind(ipp)

    replica_thread = threading.Thread(target=replica.listen).start()
    leader_thread = threading.Thread(target=leader.listen).start()
    acceptor_thread = threading.Thread(target=acceptor.listen).start()

    print('Server ready....')
    
    while True:
        data, addr = s.recvfrom(1024)
        print('Server received message from', addr)
        response = handle(data.decode('utf-8'))
        if response:
            s.sendto(response.encode('utf-8'), addr)

except KeyboardInterrupt:
    s.close()
    print('Interrupted')
    sys.exit(1)
