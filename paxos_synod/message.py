""" The following code generalizes messages on the Simple Paxos driven network."""

# Import the necessary libraries.
import json
import sys
from typing import Literal

# Class Definitions
class Message:
    # Initializer
    def __init__ (self, sender_id: int, receiver_id: int, message_type: Literal['prepare', 'promise', 'accept-request', 'ack']):
        """
            Initializes message with following attributes:
                sender_id: int
                    Unique ID of the sender.
                receiver_id: int
                    Unique ID of the receiver.
        """

        # Assert that the message type is valid
        assert message_type in ['prepare', 'promise', 'accept-request', 'ack']

        # Initialize message headers
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message_type = message_type

# Prepare Class
class Prepare(Message):
    # Initializer
    def __init__ (self, sender_id: int, receiver_id: int, proposal_number: int):
        """
            Initializes prepare message with following attributes:
                proposal_number: int
                    The number of the proposal.
        """

        # Initialize message headers
        super().__init__(sender_id, receiver_id, 'prepare')

        # Initialize prepare message details
        self.proposal_number = proposal_number

# Promise Class
class Promise(Message):
    # Initializer
    def __init__ (self, sender_id: int, receiver_id: int, proposal_number: int, prev_accepted_number: int | None, prev_accepted_value: int | None, result: Literal['accepted', 'rejected']):
        """
            Initializes promise message with following attributes:
                proposal_number: int
                    The number of the proposal.
                prev_accepted_number: int
                    The number of the highest numbered proposal that has been "accepted",
                    i.e. the proposal number of the last consensus value.
                prev_accepted_value: *
                    The last consensus value.
        """

        # Initialize message headers
        super().__init__(sender_id, receiver_id, 'promise')

        # Assert that the result type is valid
        assert result in ['accepted', 'rejected']

        # Initialize promise message details
        self.result = result
        self.proposal_number = proposal_number
        self.prev_accepted_number = prev_accepted_number
        self.prev_accepted_value = prev_accepted_value

# AcceptRequest Class
class AcceptRequest(Message):
    # Initializer
    def __init__ (self, sender_id: int, receiver_id: int, proposal_number: int, value: int):
        """
            Initializes accept-request message with following attributes:
                proposal_number: int
                    The number of the proposal.
                value: *
                    The value that is being proposed.
        """

        # Initialize message headers
        super().__init__(sender_id, receiver_id, 'accept-request')

        # Initialize accept-request message details
        self.proposal_number = proposal_number
        self.value = value

# Response to AcceptRequest
# Sent from Acceptor to Proposer
class Ack(Message):
    # Initializer
    def __init__ (self, sender_id: int, receiver_id: int, consensus_number: int, consensus_value: int, result: Literal['accepted', 'rejected']):
        """
            Initializes ack message with following attributes:
                proposal_number: int
                    The number of the proposal.
        """

        # Initialize message headers
        super().__init__(sender_id, receiver_id, 'ack')

        # Assert that the result type is valid
        assert result in ['accepted', 'rejected']

        # Initialize ack message details
        self.result = result
        self.consensus_number = consensus_number
        self.consensus_value = consensus_value
