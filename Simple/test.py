# Testing Paxos with 2 nodes (1 with proposer initialized, 1 with acceptor initialized):
# Path: Simple/test.py

# Import the necessary libraries.
from message import Message, Prepare, Promise, AcceptRequest, Ack
# from proposer import Proposer
# from acceptor import Acceptor
from node import Node
import threading
from dir import *
import os
import time


if __name__ == '__main__':
    # Initialize proposer and acceptor
    proposer1 = Node(1, 2, [3,4,5], 3, randomize_acceptors=True, wait_time=0.5, proposal_value=1)
    proposer2 = Node(2, 2, [3,4,5], 3, randomize_acceptors=True, wait_time=0.5, proposal_value=2)
    acceptor1 = Node(3, 2, [3,4,5], 3, randomize_acceptors=True, wait_time=0.5)
    acceptor2 = Node(4, 2, [3,4,5], 3, randomize_acceptors=True, wait_time=0.5)
    acceptor3 = Node(5, 2, [3,4,5], 3, randomize_acceptors=True, wait_time=0.5)

    # Initialize threads that listen to messages
    proposer_thread1 = threading.Thread(target=proposer1.listen)
    proposer_thread2 = threading.Thread(target=proposer2.listen)
    acceptor_thread1 = threading.Thread(target=acceptor1.listen)
    acceptor_thread2 = threading.Thread(target=acceptor2.listen)
    acceptor_thread3 = threading.Thread(target=acceptor3.listen)

    # Start threads
    proposer_thread1.start()
    proposer_thread2.start()
    acceptor_thread1.start()
    acceptor_thread2.start()
    acceptor_thread3.start()

    # Proposer proposes value 1

    t1 = threading.Thread(target=proposer1.propose, args=(1,))
    # consensus = proposer1.propose(1)
    # time.sleep(0.5)
    # print("-------------------------Consensus value: ", consensus)
    t2 = threading.Thread(target=proposer2.propose, args=(2,)) 

    t1.start()
    time.sleep(1)
    t2.start()


    print("---------proof---------")
    t1.join()
    t2.join()
    # consensus = proposer2.propose(2)
    # print("-------------------------Consensus value: ", consensus)

    # End program
    os._exit(0)