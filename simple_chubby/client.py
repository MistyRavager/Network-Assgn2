# import sys
# import os
# import time
import json
# import threading
import socket


class Client:
    def __init__(self, server_port: int, server_host: str, id: int) -> None:
        self.server_port = server_port
        self.server_host = server_host
        self.id = id

    def send_request(self) -> str:
        '''
        Sends lock request to server
        Message format: {"type": "request", "id": id}
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            message = json.dumps({"type": "request", "id": self.id})
            s.sendall(message.encode())
            data = s.recv(1024)
            if data:
                return data.decode('utf-8')
            
    def send_keepalive(self) -> str:
        '''
        Sends keepalive to server
        Message format: {"type": "keepalive", "id": id}
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            message = json.dumps({"type": "keepalive", "id": self.id})
            s.sendall(message.encode())
            data = s.recv(1024)
            if data:
                return data.decode('utf-8')
    
    def handle_request(self, message: str) -> bool:
        '''
        Handles response from server for lock request
        '''
        message = json.loads(message)
        if message['value'] == 'ack':
            print(f'Lock granted for {self.id}')
            return True
        else:
            print(f'Lock denied for {self.id}')
            return False
        
    def handle_keepalive(self, message: str) -> bool:
        '''
        Handles response from server for keepalive
        '''
        message = json.loads(message)
        if message['value'] == 'ack':
            print(f'Keepalive ack for {self.id}')
            return True
        else:
            print(f'Keepalive nak for {self.id}')
            return False