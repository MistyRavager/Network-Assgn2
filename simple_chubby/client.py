# import sys
# import os
import time
import json
# import threading
import socket
from typing import Literal


class Client:
    def __init__(self, server_port: int, server_host: str, id: int, sleep_time: int) -> None:
        self.server_port = server_port
        self.server_host = server_host
        self.id = id
        self.sleep_time = sleep_time

    def send_message(self, type: Literal['request', 'keepalive']) -> str:
        '''
        Sends message to server
        Message format: {"type": "request"/"keepalive", "id": id}
        Returns response from server
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            message = {
                'type': type,
                'id': self.id
            }
            s.sendto(json.dumps(message).encode(), (self.server_host, self.server_port))
            data, addr = s.recvfrom(1024)
            if addr == (self.server_host, self.server_port):
                return data.decode()
            else:
                return None
        
            
    
    def handle_lock_response(self, message: str) -> bool:
        '''
        Handles lock response from server for lock request
        '''
        message = json.loads(message)
        if message['value'] == 'ack':
            print(f'Lock granted for {self.id}')
            return True
        else:
            print(f'Lock denied for {self.id}')
            return False
        
    def handle_keepalive_response(self, message: str) -> bool:
        '''
        Handles response from server for keepalive
        '''
        message = json.loads(message)
        if message['value'] == 'ack':
            print(f'Keepalive ack for {self.id}')
            time.sleep(self.sleep_time)
            return True
        else:
            print(f'Keepalive nak for {self.id}')
            return False