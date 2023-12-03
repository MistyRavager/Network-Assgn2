# import sys
# import os
import time
# import json
import threading


class Server:
    def __init__(self, port: int, host: str, timeout_limit: int) -> None:
        self.port = port
        self.host = host
        self.num_locks = 10
    
        self.lock = [threading.Lock() for _ in range(self.num_locks)]
        self.current_master = [None] * self.num_locks
        self.last_keepalive = [None] * self.num_locks
        self.timeout_limit = timeout_limit

    def get_current_master(self, lock_num: int) -> int:
        if (lock_num < 0) or (lock_num >= self.num_locks):
            return -1
        with self.lock[lock_num]:
            return self.current_master[lock_num]

    def timeout(self, lock_num: int) -> None:
        with self.lock[lock_num]:
            if self.last_keepalive[lock_num] is None:
                # nothing to do
                return
            elif time.time() - self.last_keepalive[lock_num] > self.timeout_limit:
                # no keepalive received from current master, so reset
                self.current_master[lock_num] = None
                self.last_keepalive[lock_num] = None

    def handle_keepalive(self, id: int, lock_num: int) -> bool:
        with self.lock[lock_num]:
            if self.current_master[lock_num] == id:
                self.last_keepalive[lock_num] = time.time()
                return True
            else:
                return False

    def handle_request(self, id: int, lock_num: int) -> bool:
        with self.lock[lock_num]:
            if self.current_master[lock_num] is None:
                self.current_master[lock_num] = id
                self.last_keepalive[lock_num] = time.time()
                return True
            else:
                return False
