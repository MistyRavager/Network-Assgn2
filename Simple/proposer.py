""" The following code is the class for the proposer process for the Paxos algorithm. """

# Import the necessary libraries.
from message import *
import json
import socket
import sys
import threading
import random
from typing import Tuple, List

# Class Definitions
class Proposer:
    # Initializer
    def __init__ (self, id:int, nproposers:int, acceptors:List[int], nacceptors:int, exponential_backoff:bool=False, randomize_acceptors:bool=False, wait_time:float|None=None):
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

        # Initialize proposal number and value
        self.proposal_number = 0
        self.value = 0
        self.prev_number = 0
        self.prev_value = 0

        # Initialize acceptor details
        self.accepted_count = 0
        self.rejected_count = 0
        self.majority_list = []

    # Function to generate a majority list of acceptors
    def generate_majority(self) -> List[int]:
        """
            Generates a majority list of acceptors to send prepare message to.
        """

        # Minimum Majority Value & Determine selection value
        min_majority = (self.nacceptors + 1) // 2
        select = random.randint(min_majority, self.nacceptors)

        # Return a random sample of acceptors
        return random.sample(self.acceptors, select)

    # Function to prepare proposal
    def prepare_proposal(self, value: int) -> Tuple[int, List[int]]:
        """
            Prepares proposal by sending prepare message to acceptors.
            Also identifies a majority of acceptors to send message to.
        """

        # Increment proposal number
        self.proposal_number += 1

        # Generate majority list of acceptors
        majority = self.generate_majority()
        self.majority_list = majority

        # Return proposal number and majority list
        return self.proposal_number, majority
    
    # Function to send a an accept-request message to acceptors
    def send_accept_request(self, proposal_number: int, value: int, majority: List[int]) -> Tuple[int, int, List[int]]:
        """
            Sends accept-request message to acceptors.
            Also identifies a majority of acceptors to send message to.
        """

        # Iterate through majority list to send accept-request message
        for acceptor in self.majority_list:
            commit = AcceptRequest(self.id, acceptor, proposal_number, value)
            #Send Commit Message : TBD

    # Check if rejected
    def is_rejected(self) -> bool:
        """
            Checks if proposal has been rejected.
        """

        return self.rejected_count >= (self.nacceptors + 1) // 2
    
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

            # If majority of acceptors have accepted
            if self.accepted_count >= (self.nacceptors + 1) // 2:
                # Send accept-request message
                # Interrupt sleep (TBD)
                pass

        # If promise-reject message received
        elif (type(message) == Promise) and (self.proposal_number == message.proposal_number) and (message.result == 'rejected'):
            # Increment rejected count
            self.rejected_count += 1

            # If majority of acceptors have rejected
            if self.rejected_count >= (self.nacceptors + 1) // 2:
                # Send prepare message
                # Interrupt sleep (TBD)
                pass

        # If ack-accept message received
        elif (type(message) == Ack) and (self.proposal_number == message.proposal_number) and (message.result == 'accepted'):
            pass

        # If ack-reject message received
        elif (type(message) == Ack) and (self.proposal_number == message.proposal_number) and (message.result == 'rejected'):
            pass
