import sys
import os
import time
import json
import threading


class Server:
    def __init__(self, port: int, host: int, timeout_limit: int) -> None:
        self.port = port
        self.host = host
        self.lock = threading.Lock()
        self.current_master = None
        self.last_ack = None
        self.timeout_limit = timeout_limit

    def get_current_master(self):
        self.lock.acquire()
        master = self.current_master
        self.lock.release()
        return master

    def timeout(self):
        self.lock.acquire()
        if self.last_ack is not None:
            if time.time() - self.last_ack > self.timeout_limit:
                self.current_master = None
                self.last_ack = None
        self.lock.release()

    def set_ack(self, id: int):
        self.lock.acquire()
        if self.current_master == id:
            self.last_ack = time.time()
        self.lock.release()

    def handle_request(self, id: int): 
        self.lock.acquire()
        if self.current_master is None:
            self.current_master = id
            self.last_ack = time.time()
            self.lock.release()
            return True
        else:
            self.lock.release()
            return False