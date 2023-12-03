""" The following code describes a node in a Simple Paxos driven network. """

# Import the necessary libraries.
import json
import socket
import sys
import threading
import random
from Simple.proposer import Proposer
from Simple.acceptor import Acceptor
from Simple.message import *
from dir import *
from typing import Tuple

# Class Definitions
class Node:
    def __init__(self, id:int, exponential_backoff:bool=False, randomize_acceptors:bool=False, wait_time:float=None):
        """
        Initialize node

        params:
            id: int
                node id
            exponential_backoff: bool
                whether to use exponential backoff
            randomize_acceptors: bool
                whether to randomize acceptors
            wait_time: float
                wait time for random mode
        """

        # ID
        self.id = id

        # Initialize proposer and acceptor
        self.proposer = Proposer(id, len(dir_proposers), dir_acceptors, len(dir_acceptors), exponential_backoff, randomize_acceptors, wait_time)
        self.acceptor = Acceptor(id, len(dir_acceptors))

        # Initialize host
        self.hostname, self.port = dir_net[id]

        # Initialize UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.hostname, self.port))
        
    # Function to propose a value
    def propose(self, value) -> None:
        """
        Proposes a value to the acceptors.
        """

        # Propose the value
        while(True):
            # Prepare proposal
            self.proposer.prepare_proposal(value)

            # Wait till interrupted by proposer
            # TBD

            # Check if proposal was rejected
            if self.proposer.rejected():
                # If proposal was rejected, try again
                continue
            else:
                # If proposal was accepted, break
                self.proposer.send_accept_request() # Fill params
                # Sleep

            # Check if ack was rejected
            # Then continue

            # Else break
    
    # Handler
    def handle(self, message: Message) -> None:
        if(type(message) == Promise) or (type(message) == Ack):
            self.proposer.handle(message)
        elif(type(message) == Prepare) or (type(message) == AcceptRequest):
            self.acceptor.handle(message)
        # Learner's handle
            




