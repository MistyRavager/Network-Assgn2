import json
from classes import *
import dataclasses
import threading
from typing import List, Tuple
from socket import *
from dir import *

class Acceptor():
    def __init__(self, id: int) -> None:
        self.id = id
        self.ballot_num = Ballot(-1, -1) # Uninit
        self.accepted: List[Tuple[int, Ballot, Command]] = [] # List of (slot, ballot_num, command).

        self.lock_accepted = threading.Lock() # Sync things
        self.lock_ballot_num = threading.Lock()

    def receive_proposal(self, message: P1A):
        """
        Phase 1.
        Input is prepare, output is a promise
        """
        with self.lock_ballot_num:
            if message.ballot > self.ballot_num:
                self.ballot_num = message.ballot_num
            return P1B(MessageType.P1B, message.ballot.leader_id, self.id, self.ballot_num, self.accepted)
        # TODO: UDP packet size < accepted

    def receive_accept_request(self, message: P2A):
        """
        Phase 2
        Input is accept-request, output is an ack
        """
        with self.lock_accepted:
            with self.lock_ballot_num:
                if message.ballot_num == self.ballot_num:
                    self.accepted += [(message.slot, message.ballot_num, message.command)]
                return P2B(MessageType.P2B, message.leader_id, self.id, self.ballot_num)
        
    def handle(self, message: Message):
        """
            Handles received message from proposer.
        """
        if message.type == MessageType.P1A:
            msg = self.receive_proposal(message)
        
        # If accept-request message received
        elif message.type == MessageType.P2A:
            msg = self.receive_accept_request(message)
        
        return msg
    
    def listen(self):
        ipp = acceptors[self.id]
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(ipp)

        while True:
            data, addr = sock.recvfrom(1024)
            msg = json.loads(data.decode('ascii'))
            msg = Message.from_json(msg)

            # print(f"{self.id}: Received {msg} from {addr}")

            res = self.handle(msg)

            # print(f"{self.id}: Sending {msg} to {addr}")
            
            sock.sendto(json.dumps(dataclasses.asdict(res)).encode('ascii'), addr)
            
            # print(f"{self.id}: Sent {msg} to {addr}")
