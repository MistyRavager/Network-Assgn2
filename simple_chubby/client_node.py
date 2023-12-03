from client import Client
import json

server_port = 5000
server_host = 'localhost'

client = Client(server_port, server_host, 1, 3)
message_type = 'request'
while True:
    message = client.send_message(message_type)
    if message_type == 'request':
        if client.handle_lock_response(message):
            message_type = 'keepalive'
        else:
            break
    elif message_type == 'keepalive':
        if client.handle_keepalive_response(message):
            message_type = 'keepalive'
        else:
            break
    else:
        print('Invalid message type')
        break

print('Client exiting')