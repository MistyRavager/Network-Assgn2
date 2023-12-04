""" The following code describes a node in a Simple Paxos driven network. """

# Import the necessary libraries.
import json
import socket
import sys
import threading
import random
from proposer import Proposer
from acceptor import Acceptor
from message import *
from dir import *
from typing import Tuple, List
import time
from termcolor import colored
from termcolor import colored

class Node:
    def __init__(
            self, 
            id:int, 
            nproposers:int,
            acceptors:List[int],
            nacceptors:int,
            exponential_backoff:bool=False, 
            randomize_acceptors:bool=False, 
            wait_time:float=None,
            proposal_value:int=None,
        ):
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
                wait time before retrying
        """

        # ID
        self.id = id

        self.wait_time = wait_time
        self.timer = Sleep(self.wait_time)

        # Initialize proposer and acceptor
        self.proposer = Proposer(id, nproposers, acceptors, nacceptors, exponential_backoff, randomize_acceptors, wait_time, self.timer)
        self.acceptor = Acceptor(id, nacceptors)

        # Initialize host
        self.hostname, self.port = dir_net[id]
        
        self.backoff_num = 0
        self.exponential_backoff = exponential_backoff
        
        self.backoff_num = 0
        self.exponential_backoff = exponential_backoff

        # Initialize UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.hostname, self.port))
        # self.proposal_value = proposal_value
        
    # Function to propose a value
    def propose(self, value:int) -> int:
        """
        Proposes a value to the acceptors.
        """

        # Propose the value
        while(True):
            # Prepare proposal
            prop_list = self.proposer.prepare_proposal(value)
            prop_json_list = [self.msg_jsonify(prop) for prop in prop_list]

            # Send proposal to acceptors
            for prop_idx, prop_json in enumerate(prop_json_list):
                # print(f"{self.id}: Sending {prop_json} to {dir_net[prop_list[prop_idx].receiver_id]}")
                self.sock.sendto(json.dumps(prop_json).encode('ascii'), dir_net[prop_list[prop_idx].receiver_id])
                proposer, acceptor = colored(f"Proposer {self.id}", 'green'), colored(f"Acceptor {prop_list[prop_idx].receiver_id}", 'red')
                log_msg = f"{proposer}: Sent {prop_json} to {dir_net[prop_list[prop_idx].receiver_id]} ({acceptor})"
                print(log_msg)


            # Wait till interrupted by proposer
            self.timer.sleep()
            time.sleep(0.2)
            # Check if proposal was rejected
            if self.proposer.is_rejected():
                # If proposal was rejected, try again
                if self.exponential_backoff:
                    time.sleep(0.1*random.randint(1, 2**self.backoff_num))
                    self.backoff_num += 1
                    log_msg = colored(f"{self.id}: Backoff num: {self.backoff_num}", 'yellow')
                    print(log_msg)
                if self.exponential_backoff:
                    time.sleep(0.1*random.randint(1, 2**self.backoff_num))
                    self.backoff_num += 1
                    log_msg = colored(f"{self.id}: Backoff num: {self.backoff_num}", 'yellow')
                    print(log_msg)
                continue
            else:
                # Proposal is accepted
                acc_list = self.proposer.send_accept_request(value) # Fill params
                acc_json_list = [self.msg_jsonify(acc) for acc in acc_list]
                print(acc_json_list)
                print(acc_list)
                for acc_idx, acc_json in enumerate(acc_json_list):
                    # print(f"Proposer {self.id}: Sending acc req lno 91 {acc_json} to {dir_net[acc_list[acc_idx].receiver_id]}")
                    self.sock.sendto(json.dumps(acc_json).encode('ascii'), dir_net[acc_list[acc_idx].receiver_id])
                    # print(f"Proposer {self.id}: Sent acc req {acc_json} to {dir_net[acc_list[acc_idx].receiver_id]} (Acceptor {acc_list[acc_idx].receiver_id})\n")
                    proposer, acceptor = colored(f"Proposer {self.id}", 'green'), colored(f"Acceptor {acc_list[acc_idx].receiver_id}", 'red')
                    log_msg = f"{proposer}: Sent {acc_json} to {dir_net[acc_list[acc_idx].receiver_id]} ({acceptor})"
                    print(log_msg)
                    # print(f"Proposer {self.id}: Sent acc req {acc_json} to {dir_net[acc_list[acc_idx].receiver_id]} (Acceptor {acc_list[acc_idx].receiver_id})\n")
                    proposer, acceptor = colored(f"Proposer {self.id}", 'green'), colored(f"Acceptor {acc_list[acc_idx].receiver_id}", 'red')
                    log_msg = f"{proposer}: Sent {acc_json} to {dir_net[acc_list[acc_idx].receiver_id]} ({acceptor})"
                    print(log_msg)
            # Wait till interrupted by proposer
            self.timer.sleep()

            # Check if ack was rejected
            if self.proposer.is_rejected():
                # Try try again!
                if self.exponential_backoff:
                    time.sleep(0.1*random.randint(1, 2**self.backoff_num))
                    self.backoff_num += 1
                    log_msg = colored(f"{self.id}: Backoff num: {self.backoff_num}", 'yellow')
                    print(log_msg)
                    # print(f"{self.id}: Backoff num: {self.backoff_num}\n")
                if self.exponential_backoff:
                    time.sleep(0.1*random.randint(1, 2**self.backoff_num))
                    self.backoff_num += 1
                    log_msg = colored(f"{self.id}: Backoff num: {self.backoff_num}", 'yellow')
                    print(log_msg)
                    # print(f"{self.id}: Backoff num: {self.backoff_num}\n")
                continue

            else:
                print("\n\n----------------------END------------------------\n\n")
                print("\n\n----------------------END------------------------\n\n")
                return self.proposer.consensus_value
            

            # Then continue

            # Else break
    
    # Function to receive message
    
    # Handler
    def handle(self, message: Message) -> None:
        if(type(message) is Promise) or (type(message) is Ack):
            self.proposer.handle(message)
        elif(type(message) is Prepare) or (type(message) is AcceptRequest):
            recv_msg = self.acceptor.handle(message)
            # print(f'Sender: {message.sender_id}, Receiver: {message.receiver_id}')
            # print(f'Sender: {message.sender_id}, Receiver: {message.receiver_id}')
            if recv_msg is not None:
                self.sock.sendto(json.dumps(self.msg_jsonify(recv_msg)).encode('ascii'), dir_net[recv_msg.receiver_id])
                proposer, acceptor = colored(f"Acceptor {self.id}", 'red'), colored(f"Proposer {recv_msg.receiver_id}", 'green')
                log_msg = f"{proposer}: Sent {self.msg_jsonify(recv_msg)} to {dir_net[recv_msg.receiver_id]} ({acceptor})"
                print(log_msg)
                # print(f'Acceptor {self.id}: Response: Sending {self.msg_jsonify(recv_msg)} to {dir_net[recv_msg.receiver_id]} (Proposer {recv_msg.receiver_id}))\n')
                proposer, acceptor = colored(f"Acceptor {self.id}", 'red'), colored(f"Proposer {recv_msg.receiver_id}", 'green')
                log_msg = f"{proposer}: Sent {self.msg_jsonify(recv_msg)} to {dir_net[recv_msg.receiver_id]} ({acceptor})"
                print(log_msg)
                # print(f'Acceptor {self.id}: Response: Sending {self.msg_jsonify(recv_msg)} to {dir_net[recv_msg.receiver_id]} (Proposer {recv_msg.receiver_id}))\n')

        # Learner's handle

    def listen(self):
        """
        Listens for messages from other nodes.
        """
        while True:
            if self.id in self.proposer.acceptors:
                if self.acceptor.has_accepted:
                    log_msg = colored(f"\n----------Acceptor {self.id}: Consensus value: {self.acceptor.accepted_value}----------\n", 'yellow')
                    print(log_msg)
                    # print(f'\n----------Acceptor {self.id}: Consensus value: {self.acceptor.accepted_value}----------\n')
            if self.id in self.proposer.acceptors:
                if self.acceptor.has_accepted:
                    log_msg = colored(f"\n----------Acceptor {self.id}: Consensus value: {self.acceptor.accepted_value}----------\n", 'yellow')
                    print(log_msg)
                    # print(f'\n----------Acceptor {self.id}: Consensus value: {self.acceptor.accepted_value}----------\n')
                else:
                    log_msg = colored(f"\n----------Acceptor {self.id}: Consensus value: None----------\n", 'yellow')
                    print(log_msg)
                    # print(f'\n----------Acceptor {self.id}: Consensus value: None----------\n')

                    log_msg = colored(f"\n----------Acceptor {self.id}: Consensus value: None----------\n", 'yellow')
                    print(log_msg)
                    # print(f'\n----------Acceptor {self.id}: Consensus value: None----------\n')

            # Receive message
            data, addr = self.sock.recvfrom(1024)

            message = json.loads(data.decode('ascii'))

            # Handle message
            # print(addr)
            if addr[0] == '127.0.0.1':
                addr = ('localhost', addr[1])
            self.handle(self.msg_parse(message, addr))
            # if self.acceptor.has_accepted:
            #     print(f'Accepted: {self.acceptor.accepted_value}')
            print("shouldnt print sometime")

        print("shouldnt print anytime whatsoever")

    def msg_jsonify(self, message: Message):
        """
        Converts a message to a json
        """
        if type(message) == Prepare:
            return {'type': 'prepare', 'proposal_number': message.proposal_number}
        elif type(message) == Promise:
            return {'type': 'promise', 'proposal_number': message.proposal_number, 'prev_accepted_number': message.prev_accepted_number, 'prev_accepted_value': message.prev_accepted_value, 'result': message.result}
        elif type(message) == AcceptRequest:
            return {'type': 'accept-request', 'proposal_number': message.proposal_number, 'value': message.value}
        elif type(message) == Ack:
            return {'type': 'ack', 'consensus_number': message.consensus_number, 'consensus_value': message.consensus_value, 'result': message.result}


    def msg_parse(self, message: dict, addr: Tuple) -> Message:
        """
        Converts a json to a message
        """
        for key, value in dir_net.items():
            if value == addr:
                sender_id = key
                break
        if message['type'] == 'prepare':
            return Prepare(sender_id, self.id, message['proposal_number'])
        elif message['type'] == 'promise':
            return Promise(sender_id, self.id, message['proposal_number'], message['prev_accepted_number'], message['prev_accepted_value'], message['result'])
        elif message['type'] == 'accept-request':
            return AcceptRequest(sender_id, self.id, message['proposal_number'], message['value'])
        elif message['type'] == 'ack':
            return Ack(sender_id, self.id, message['consensus_number'], message['consensus_value'], message['result'])
            




