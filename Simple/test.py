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


if __name__ == '__main__':
    # Initialize proposer and acceptor
    proposer = Node(1, 1, [2], 1, randomize_acceptors=True, wait_time=0.5, proposal_value=1)
    acceptor = Node(2, 1, [2], 1, randomize_acceptors=True, wait_time=0.5)

    # Initialize threads that listen to messages
    proposer_thread = threading.Thread(target=proposer.listen)
    acceptor_thread = threading.Thread(target=acceptor.listen)

    # Start threads
    proposer_thread.start()
    acceptor_thread.start()

    # Proposer proposes value 1
    consensus = proposer.propose(1)
    print("Consensus value: ", consensus)

    # End program
    os._exit(0)