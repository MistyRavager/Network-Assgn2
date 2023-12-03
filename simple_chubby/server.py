import sys
import os
import time
import json
import threading


class Server:
    def __init__(self, port: int, host: str, timeout_limit: int) -> None:
        self.port = port
        self.host = host
        self.lock = threading.Lock()
        self.current_master = None
        self.last_keepalive = None
        self.timeout_limit = timeout_limit

    def get_current_master(self):
        with self.lock:
            return self.current_master

    def timeout(self):
        with self.lock:
            if self.last_keepalive is None:
                # nothing to do
                return
            elif time.time() - self.last_keepalive > self.timeout_limit:
                # no keepalive received from current master, so reset
                self.current_master = None
                self.last_keepalive = None

    def handle_keepalive(self, id: int):
        with self.lock:
            if self.current_master == id:
                self.last_keepalive = time.time()

    def handle_request(self, id: int):
        with self.lock:
            if self.current_master is None:
                self.current_master = id
                self.last_keepalive = time.time()
                return True
            else:
                return False
