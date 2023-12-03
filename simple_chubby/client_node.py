from client import Client
import time
import threading
import socket
import sys

server_port = 5000
server_host = '127.0.0.1'

client = Client(server_port, server_host, 1, 3)

def send_keepalive():
    global client
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        message = client.make_message('keepalive')
        s.sendto(message.encode(), (server_host, server_port))
        response, addr = s.recvfrom(1024)
        print(response, addr)
        if addr == (server_host, server_port):
            if client.check_keepalive_response(response.decode()):
                time.sleep(client.sleep_time)
            else:
                s.close()
                return
        else :
            s.close()
            print('Invalid response')
            return

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Client ready....')

    while True:
        message = client.make_message('request')
        print(message)
        s.sendto(message.encode(), (server_host, server_port))
        response, addr = s.recvfrom(1024)
        print("-------------------")
        print(response, addr)
        print("-------------------")
        if addr == (server_host, server_port):
            if client.check_lock_response(response.decode()):
                send_keepalive()
                # t=threading.Thread(target=send_keepalive)
                # t.start()
                # t.join()
                # client = Client(server_port, server_host, client.id+1, client.sleep_time)
        else:
            print('Invalid response')
            break

except KeyboardInterrupt:
    s.close()
    print('Client closed since keyboard interrupt')
    sys.exit(1)

