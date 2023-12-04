from Complex.messages_acc import *
import threading

class Acceptor():
    def __init__(self, id) -> None:
        self.id = id
        self.ballot_num = -1 # Uninit
        self.accepted = [] # List of (ballot_num, slot, command).

        self.lock_accepted = threading.Lock() # Sync things
        self.lock_ballot_num = threading.Lock()

    def receive_proposal(self, message: Prepare):
        """
        Phase 1.
        Input is prepare, output is a promise
        """
        with self.lock_ballot_num:
            if message.ballot_num > self.ballot_num:
                self.ballot_num = message.ballot_num
            return Promise(message.sender_id, self.id, self.ballot_num, self.accepted)
        # TODO: UDP packet size < accepted

    def receive_accept_request(self, message: AcceptRequest):
        """
        Phase 2
        Input is accept-request, output is an ack
        """
        with self.lock_accepted:
            with self.lock_ballot_num:
                if message.ballot_num == self.ballot_num:
                    self.accepted += [(message.ballot_num, message.slot, message.command)]
            return Ack(message.sender_id, self.id, self.ballot_num)
        
    def handle(self, message: Message):
        """
            Handles received message from proposer.
        """
        if type(message) is Prepare:
            msg = self.receive_proposal(message)
        
        # If accept-request message received
        elif type(message) is AcceptRequest:
            msg = self.receive_accept_request(message)
        
        return msg