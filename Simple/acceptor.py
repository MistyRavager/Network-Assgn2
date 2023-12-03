""" The following code is the class for the acceptor process for the Paxos algorithm. """

# Import the necessary libraries.
from message import *
import json
import socket
import sys
import threading
from typing import Tuple

# Class Definitions
class Acceptor:
    # Initializer
    def __init__ (self, id:int, nacceptors:int):
        """
            Initializes acceptor process with following attributes:
                id: int
                    Unique ID of every acceptor.
                nacceptors: int
                    Total number of acceptors to keep track of majority.
                promised_number: int
                    The number of the highest numbered proposal it has "adopted".
                    Consequently, all the proposals numbered less than this number
                    will be ignored/rejected by the acceptor.
                accepted_number: int
                    The number of the highest numbered proposal it has "accepted".
                accepted_value: *
                    The present consensus value.
                has_accepted: bool
                    Whether the acceptor has accepted a value or not.
        """

        # Initialize host details
        self.id = id
        self.nacceptors = nacceptors

        self.lock_acc_num = threading.Lock()
        self.lock_acc_val = threading.Lock()
        self.lock_pro_num = threading.Lock()

        # Initialize promise number and accepted value pair
        self.promised_number = 0
        self.accepted_number = 0
        self.accepted_value = 0
        self.has_accepted = False
    
    # Function to receive messages from proposer
    def receive_proposal(self, message:Prepare) -> None:
        """
            Receives proposal from proposer. If the proposal number does not exceed
            the promised number, the proposal is rejected.
            Otherwise, the proposal is accepted and the promised number is accepted.
            If the acceptor has already accepted a value, it also sends the accepted 
            number-value pair to the proposer.
            We then send the Promise back to the proposer.
        """

        self.lock_pro_num.acquire()
        if message.proposal_number <= self.promised_number:
            prom = Promise(self.id, message.sender_id, self.promised_number, None, None, 'rejected')
        else:
            self.promised_number = message.proposal_number
            self.lock_acc_num.acquire()
            self.lock_acc_val.acquire()
            if self.has_accepted:
                prom = Promise(self.id, message.sender_id, self.promised_number, self.accepted_number, self.accepted_value, 'accepted')
            else:
                prom = Promise(self.id, message.sender_id, self.promised_number, None, None, 'accepted')
            self.lock_acc_val.release()
            self.lock_acc_num.release()

        self.lock_pro_num.release()
        # Send prom
        # TBD

    # Function to receive accept message from proposer
    def receive_accept_request(self, message:AcceptRequest) -> None:
        """
            Receives accept-request message from proposer. If the proposal number 
            does not exceed the promised number, the proposal is rejected.
            Otherwise, the proposal is accepted and the promised number is accepted.
            The accepted number-value pair is also updated.
        """

        """
            We are assuming that the proposers are not adversarial and will not send
            accept-request messages with proposal numbers less than the promised number.
        """
        
        self.lock_pro_num.acquire()
        if message.proposal_number < self.promised_number:
            ack = Ack(self.id, message.sender_id, self.accepted_number, self.accepted_value, 'rejected')
        else:
            self.lock_acc_num.acquire()
            self.lock_acc_val.acquire()
            self.has_accepted = True
            self.promised_number = message.proposal_number
            self.accepted_number = message.proposal_number
            self.accepted_value = message.value
            ack = Ack(self.id, message.sender_id, self.accepted_number, self.accepted_value, 'accepted')
            self.lock_acc_val.release()
            self.lock_acc_num.release()

        self.lock_pro_num.release()
        # Send ack
        # TBD
    
    # Main Handler Function
    def handle(self, message:Message) -> None:
        """
            Handles received message from proposer.
        """

        # If prepare message received
        if type(message) == Prepare:
            self.receive_proposal(message)
        
        # If accept-request message received
        elif type(message) == AcceptRequest:
            self.receive_accept_request(message)
