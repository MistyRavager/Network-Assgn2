"""
Code that demonstrates the need for exponential backoff (as in CSMA/CD) : live lock
"""

# Testing Paxos with 5 nodes (2 proposers and 3 acceptors)
# Path: Simple/test.py

# Import the necessary libraries.
from message import Message, Prepare, Promise, AcceptRequest, Ack
from node import Node
import threading
from dir import *
import os
import time

def demo2(expo_backoff: bool):
    proposer_ids = [1,2]
    acceptor_ids = [3,4,5]

    backoff_state = False

    proposers = [Node(id, len(proposer_ids), acceptor_ids, len(acceptor_ids), exponential_backoff=expo_backoff, wait_time=0.05) for id in proposer_ids]
    acceptors = [Node(id, len(proposer_ids), acceptor_ids, len(acceptor_ids), exponential_backoff=expo_backoff, wait_time=0.05) for id in acceptor_ids]
    
    try:
        t = None
        for acceptor in acceptors:
            t = threading.Thread(target=acceptor.listen)
            t.start()
        for i, proposer in enumerate(proposers):
            t = threading.Thread(target=proposer.listen)
            t.start()
            t1 = threading.Thread(target=proposer.propose, args=(i+1,))
            t1.start()
            time.sleep(0.1)
        t.join()
    except KeyboardInterrupt:
        os._exit(0)
    


if __name__ == '__main__':
    # demo2(False) # This will live lock as there is no backoff
    demo2(True) # Fixes live lock
"""
Code that demonstrates the need for exponential backoff (as in CSMA/CD) : live lock
"""

# Testing Paxos with 5 nodes (2 proposers and 3 acceptors)
# Path: Simple/test.py

# Import the necessary libraries.
from message import Message, Prepare, Promise, AcceptRequest, Ack
from node import Node
import threading
from dir import *
import os
import time

def demo2(expo_backoff: bool):
    proposer_ids = [1,2]
    acceptor_ids = [3,4,5]

    backoff_state = False

    proposers = [Node(id, len(proposer_ids), acceptor_ids, len(acceptor_ids), exponential_backoff=expo_backoff, wait_time=0.05) for id in proposer_ids]
    acceptors = [Node(id, len(proposer_ids), acceptor_ids, len(acceptor_ids), exponential_backoff=expo_backoff, wait_time=0.05) for id in acceptor_ids]
    
    try:
        t = None
        for acceptor in acceptors:
            t = threading.Thread(target=acceptor.listen)
            t.start()
        for i, proposer in enumerate(proposers):
            t = threading.Thread(target=proposer.listen)
            t.start()
            t1 = threading.Thread(target=proposer.propose, args=(i+1,))
            t1.start()
            time.sleep(0.1)
        t.join()
    except KeyboardInterrupt:
        os._exit(0)
    


if __name__ == '__main__':
    # demo2(False) # This will live lock as there is no backoff
    demo2(True) # Fixes live lock