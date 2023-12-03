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

    def make_message(self, type: Literal['request', 'keepalive']) -> str:
        '''
        makes a json string to send to the server
        '''
        message = {
            'type': type,
            'id': self.id
        }
        return json.dumps(message)
    
            
    
    def check_lock_response(self, message: str) -> bool:
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
        
    def check_keepalive_response(self, message: str) -> bool:
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