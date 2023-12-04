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

    def get_latest_accepts(self) -> List[Tuple[int, Ballot, Command]]:
        """
            Returns the latest accepted commands.
        """
        out: List[Tuple[int, Ballot, Command]] = []
        slots: List[int] = []
        # with self.lock_accepted:
        #     return self.accepted

        for a in self.accepted:
            if a[0] not in slots:
                slots += [a[0]]
                out += [a]
            elif a[1] > out[slots.index(a[0])][1]:
                out[slots.index(a[0])] = a

        return out

    def receive_proposal(self, message: P1A) -> P1B:
        """
        Phase 1.
        Input is prepare, output is a promise
        """
        with self.lock_ballot_num:
            if message.ballot > self.ballot_num:
                self.ballot_num = message.ballot
            return P1B(MessageType.P1B, message.ballot.leader_id, self.id, self.ballot_num, self.get_latest_accepts())
        # TODO: UDP packet size < accepted

    def receive_accept_request(self, message: P2A) -> P2B:
        """
        Phase 2
        Input is accept-request, output is an ack
        """
        with self.lock_accepted:
            with self.lock_ballot_num:
                if message.ballot == self.ballot_num:
                    self.accepted += [(message.slot, message.ballot, message.command)]
                return P2B(MessageType.P2B, message.leader_id, self.id, self.ballot_num)
        
    def handle(self, message: dict) -> (P1B | P2B):
        """
            Handles received message from proposer.
        """
        if message["type"] == MessageType.P1A.value:
            msg = self.receive_proposal(P1A.from_dict(message))
        
        # If accept-request message received
        elif message["type"] == MessageType.P2A.value:
            msg = self.receive_accept_request(P2A.from_dict(message))
        
        return msg
    
    def listen(self):
        ipp = acceptors[self.id]
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(ipp)

        with open(f"logs/acceptor{self.id}.log", "w") as f:
            while True:
                data, addr = sock.recvfrom(1024)
                data = data.decode()
                msg = json.loads(data)

                # print(f"{self.id}: Received {msg} from {addr}")
                f.write(f"{data}\n")
                res = self.handle(msg)
                f.write(f"{data}\n")

                # print(f"{self.id}: Sending {msg} to {addr}")
                
                sock.sendto(res.to_json().encode('ascii'), addr)
                
                # print(f"{self.id}: Sent {msg} to {addr}")
