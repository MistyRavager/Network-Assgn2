""" The following code is the class for the proposer process for the Paxos algorithm. """

# Import the necessary libraries.
from message import *
import json
import socket
import sys
import threading
import random
from typing import Tuple, List
from threading import Event, Thread
from dir import *
import numpy as np

# Class Definitions
class Proposer:
    # Initializer
    def __init__ (
                self, 
                id:int, 
                nproposers:int, 
                acceptors:List[int], 
                nacceptors:int, 
                exponential_backoff:bool=False, 
                randomize_acceptors:bool=False, 
                wait_time:float|None=None,
                timer:Sleep=None,
            ):
        """
            Initializes proposer process with following attributes:
                id: int
                    Unique ID of every proposer.
                nproposers: int
                    Total number of proposers.
                acceptors: List[int]
                    List of acceptor IDs.
                nacceptors: int
                    Total number of acceptors to keep track of majority.
                exponential_backoff: bool
                    Whether to use exponential backoff.
                randomize_acceptors: bool
                    Whether to randomize acceptors.
                wait_time: float
                    Wait time between proposals in random mode.
                proposal_number: int
                    The number of the highest numbered proposal it has "made".
                value: *
                    The value that is being proposed.
                prev_number: int
                    The number of the highest numbered proposal that has been "accepted",
                    i.e. the proposal number of the last consensus value.
                prev_value: *
                    The last consensus value.
                accepted_count: int
                    The number of acceptors that have accepted the proposal.
                rejected_count: int
                    The number of acceptors that have rejected the proposal.
                majority_list: List[int]
                    The current majority list of acceptors to send prepare message to
                    or accept-request message to.
        """

        # Initialize host details
        self.id = id
        self.nacceptors = nacceptors

        # Initialize acceptor details
        self.acceptors = acceptors
        self.nacceptors = nacceptors # Maybe len(acceptors) instead?

        # Assert nacceptors is odd to ensure majority
        assert self.nacceptors % 2 == 1

        # Initialize proposer details
        self.nproposers = nproposers
        self.exponential_backoff = exponential_backoff
        self.randomize_acceptors = randomize_acceptors
        self.wait_time = wait_time

        self.timer = timer

        # Initialize proposal number and value
        self.proposal_number = id
        self.value = 0
        self.prev_number = 0
        self.prev_value = 0

        # Initialize acceptor details
        self.accepted_count = 0
        self.rejected_count = 0
        self.majority_list = []

        # Initialize max received vals and flags
        self.received_max = False
        self.max_proposal_number = float('-inf')
        self.max_value = None

        # Consensus value
        self.consensus_value = None

    # Function to generate a majority list of acceptors
    def generate_majority(self) -> List[int]:
        """
            Generates a majority list of acceptors to send prepare message to.
        """

        # Minimum Majority Value & Determine selection value
        min_majority = (self.nacceptors + 1) // 2
        if self.randomize_acceptors: 
            select = min_majority#random.randint(min_majority, self.nacceptors)
            return random.sample(sorted(self.acceptors), select)
        else: 
            select = min_majority
            return sorted(self.acceptors)[:select]
        

    # Function to prepare proposal
    def prepare_proposal(self, value: int) -> List[Prepare]:
        """
            Prepares proposal by sending prepare message to acceptors.
            Also identifies a majority of acceptors to send message to.
        """

        prepare_list = []
        self.refresh()

        # Increment proposal number
        self.proposal_number += self.nproposers

        # Generate majority list of acceptors
        majority = self.generate_majority()
        self.majority_list = majority

        for acceptor in majority:
            # Send Prepare Message : TBD
            prepare = Prepare(self.id, acceptor, self.proposal_number)
            prepare_list.append(prepare)

        # Return proposal number and majority list
        # return self.proposal_number, majority
        return prepare_list
    
    # Function to send a an accept-request message to acceptors
    def send_accept_request(self, value: int) -> List[AcceptRequest]:
        """
            Sends accept-request message to acceptors.
            Also identifies a majority of acceptors to send message to.
        """

        # Set accepted and rejected counts to default
        self.accepted_count = 0
        self.rejected_count = 0

        commit_list = []

        # Iterate through majority list to send accept-request message
        for acceptor in self.majority_list:
            if self.received_max:
                commit = AcceptRequest(self.id, acceptor, self.proposal_number, self.max_value)
                self.consensus_value = self.max_value
            else:
                commit = AcceptRequest(self.id, acceptor, self.proposal_number, value)
                self.consensus_value = value
            commit_list.append(commit)



            #Send Commit Message : TBD        
        
        return commit_list

    # Check if rejected
    def is_rejected(self) -> bool:
        """
            Checks if proposal has been rejected.
        """

        return self.accepted_count < (self.nacceptors + 1) // 2
    
    # Handle received promise message or acknowledgement from acceptors
    def handle(self, message: Message) -> None:
        """
            Handles received promise message or acknowledgement from acceptors.
            PS: Check 'consistency' here please!!!
        """

        # If promise-accept message received
        if (type(message) == Promise) and (self.proposal_number == message.proposal_number) and (message.result == 'accepted'):
            # Increment accepted count
            self.accepted_count += 1

            # Check if message has accepted number and value
            if (message.prev_accepted_number is not None) and (message.prev_accepted_value is not None):
                self.received_max = True
                # Update max proposal number and value
                if message.prev_accepted_number > self.max_proposal_number:
                    self.max_proposal_number = message.prev_accepted_number
                    self.max_value = message.prev_accepted_value

            # If majority of acceptors have accepted
            if self.accepted_count >= (self.nacceptors + 1) // 2:
                # Send accept-request message
                # Interrupt sleep 
                self.wake(self.timer)
                pass

        # If promise-reject message received
        elif (type(message) == Promise) and (self.proposal_number == message.proposal_number) and (message.result == 'rejected'):
            # Increment rejected count
            self.rejected_count += 1

            # If majority of acceptors have rejected
            if self.rejected_count >= (self.nacceptors + 1) // 2:
                # Send prepare message
                # Interrupt sleep 
                self.wake(self.timer)
                pass

        # If ack-accept message received
        elif (type(message) == Ack) and (self.proposal_number == message.consensus_number) and (message.result == 'accepted'):
            # Increment accepted count
            self.accepted_count += 1

            # If majority of acceptors have accepted
            if self.accepted_count >= (self.nacceptors + 1) // 2:
                # Send accept-request message
                # Interrupt sleep 
                self.wake(self.timer)
                pass

        # If ack-reject message received
        elif (type(message) == Ack) and (self.proposal_number == message.consensus_number) and (message.result == 'rejected'):
            # Increment rejected count
            self.rejected_count += 1

            # If majority of acceptors have rejected
            if self.rejected_count >= (self.nacceptors + 1) // 2:
                # Send prepare message
                # Interrupt sleep 
                self.wake(self.timer)
                pass
    
    def refresh(self):
        """ 
        Set values to default before new proposal
        """

        # Set received flags and max values to default
        self.received_max = False
        self.max_proposal_number = float('-inf')
        self.max_value = None

        # Set accepted and rejected counts to default
        self.accepted_count = 0
        self.rejected_count = 0
        self.consensus_value = None

    
    def wake(self, sleeper):
        """
        Wake up the Sleep object
        """
        sleeper.wake()


