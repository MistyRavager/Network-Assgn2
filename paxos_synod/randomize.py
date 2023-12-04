"""
1 proposer, 3 servers, 1 goes down
"""
# Import the necessary libraries.
from message import Message, Prepare, Promise, AcceptRequest, Ack
# from proposer import Proposer
# from acceptor import Acceptor
from node import Node
import threading
from dir import *
import os
import time

def demo1(randomize:bool):
    proposer_ids = [1]
    acceptor_ids = [3,5]

    proposers = [Node(id, len(proposer_ids), [3, 4, 5], len([3, 4, 5]), randomize_acceptors=randomize, wait_time=0.05) for id in proposer_ids]
    acceptors = [Node(id, len(proposer_ids), [3, 4, 5], len([3, 4, 5]), randomize_acceptors=randomize, wait_time=0.05) for id in acceptor_ids]
    
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
    # demo1(False) # 1 server is down, no consensus
    demo1(True) # consensus because of randomization


    # os._exit(0)

"""
1 proposer, 3 servers, 1 goes down
"""
# Import the necessary libraries.
from message import Message, Prepare, Promise, AcceptRequest, Ack
# from proposer import Proposer
# from acceptor import Acceptor
from node import Node
import threading
from dir import *
import os
import time

def demo1(randomize:bool):
    proposer_ids = [1]
    acceptor_ids = [3,5]

    proposers = [Node(id, len(proposer_ids), [3, 4, 5], len([3, 4, 5]), randomize_acceptors=randomize, wait_time=0.05) for id in proposer_ids]
    acceptors = [Node(id, len(proposer_ids), [3, 4, 5], len([3, 4, 5]), randomize_acceptors=randomize, wait_time=0.05) for id in acceptor_ids]
    
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
    # demo1(False) # 1 server is down, no consensus
    demo1(True) # consensus because of randomization


    # os._exit(0)
