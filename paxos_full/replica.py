"""
    The following code defines a class for the replicas of the Complex
    Paxos driven network. The replicas are the nodes that store values 
    modified or requested by clients. We aim to have consensus on the 
    final states of all replicas in our runs.
"""

# Importing libraries
import json
from socket import *
import threading
import dataclasses

# Importing files
from classes import *
from dir import *

import numpy as np

# Constants
SLOTS = 5

# Class Definition
class Replica:
    def __init__(self, id):
        """
            The constructor for the Replica class. It is responsible for
            initializing the replica object with the given parameters.
            id:
                The id of the replica instance - associated with host and
                port number.
            leaders:
                The list of leaders associated with the replica instance.
                To be initialized!
            state:
                The state of the replica instance. It is a dictionary that
                stores the values associated with the slots in order.
            slots:
                A list of slots that are used to store the commands to be 
                executed by the replica instance.
            slot_in:
                The least slot number that has not been proposed on.
            slot_out:
                The least slot number that has not been decided on.
            requests:
                A list of requests that are yet to be proposed.
            proposals:
                A list of proposals that are yet to be decided on.
            decisions:
                A list of decisions that have been decided on.
        """

        # Main Paramaters
        self.id = id
        self.leaders = list(range(len(leaders))) # List of leader 
        self.slots = [None] * SLOTS
        self.slot_in = 0
        self.slot_out = 0

        # State of the replica (list of Commands)
        self.state: List[Command] = []

        # List of Command objects
        self.requests: List[Command] = []

        # List of tuples (slot, Command)
        self.proposals: List[Tuple[int, Command]] = []
        self.decisions: List[Tuple[int, Command]] = []

        # Helper Parameters
        self.comm_lock = threading.Lock()


    def propose(self) -> List[Propose]:
        """
            The propose function is responsible for proposing the next 
            request in the requests list. It is called by the replica
            instance when it is ready to propose a new request.
        """

        prop_list = []

        # Checling if there are any requests to be proposed
        while len(self.requests) > 0:
            # Checking for reconfigurations??

            # Check if slot_in has been decided on
            if self.slot_in not in [i[0] for i in self.decisions]:
                # Remove first request from requests list
                req = self.requests.pop(0)

                # Make Propose object
                prop_list.append(Propose(MessageType.PROPOSE, self.slot_in, req.command))
                
                # Append to proposals list
                self.proposals.append((self.slot_in, req.command))

                # Return
                return prop_list                   
            
    
    def perform(self, command: Command) -> Response:
        """
            The perform function is responsible for performing the 
            commands in the decisions list. It is called by the replica
            instance when it is ready to perform a new command.
        """

        # Check if Command is in decisions list
        # chk = False
        # for i in self.decisions:
        #     if (i[1] == command) and (i[0] < self.slot_out):
        #         chk = True
        #         break

        # chk = np.any(self.decisions, lambda x: x[1] == command and x[0] < self.slot_out)
        
        if np.any(self.decisions, lambda x: x[1] == command and x[0] < self.slot_out):
            self.slot_out += 1
            return None

        self.state.append(command)

        # Atomic operation
        # self.comm_lock.acquire()
        # self.slots[self.slot_out] = command
        # self.slot_out += 1
        # self.comm_lock.release()

        with self.comm_lock:
            self.slots[self.slot_out] = command
            self.slot_out += 1

        # Send Response to client
        response = Response(MessageType.RESPONSE, command, 'YES')
        return response

    
    def handle(self, message) -> (List[Propose], List[Response]):
        """
            The handle function is responsible for handling the requests
            from the clients (or) decisions from the leaders. This function
            is continuously called by the replica instance to check for
            new requests or decisions.
        """

        # Return Messages
        perf: List[Response] = []
        prop: List[Propose] = []

        # Message cases
        if type(message) is Request:
            # Add to requests list
            self.requests.append(message.command)
            
        elif type(message) is Decision:
            # Add to decisions list
            self.decisions.append((message.slot, message.command))

            # While slot_out is decided on
            # chk_dec = [i for i in self.decisions if i.slot == self.slot_out]
            chk_dec = np.where(self.decisions, lambda x: x[0] == self.slot_out)
            while len(chk_dec) > 0:
                # Check for proposals
                chk_prop = np.where(self.proposals, lambda x: x[0] == self.slot_out)
                if len(chk_prop) > 0:
                    # Remove from proposals list
                    self.proposals.remove(chk_prop[0])

                    # Check is same command
                    if chk_prop[0][1] != chk_dec[0][1]:
                        # Add to requests
                        self.requests.add(chk_prop[0][1])
                    
                # Perform command
                perf.append(self.perform(chk_dec[0][1]))

                # Check for next slot
                # chk_dec = [i for i in self.decisions if i.slot == self.slot_out]
                chk_dec = np.where(self.decisions, lambda x: x[0] == self.slot_out)
            
        prop = self.propose()

        return prop, perf

    def listen(self):
        ipp = replicas[self.id]
        sock = socket(AF_INET, SOCK_DGRAM)
        print(ipp)
        sock.bind(ipp)

        with open(f"logs/replica{self.id}.log", "w") as f:
            while True:
                data, addr = sock.recvfrom(1024)
                msg = Message.from_json(data)

                # print(f"{self.id}: Received {msg} from {addr}")
                f.write(f"{msg.to_json()}\n")
                res = self.handle(msg)
                f.write(f"{res.to_json()}\n")

                # print(f"{self.id}: Sending {msg} to {addr}")
                
                sock.sendto(res.to_json().encode('ascii'), addr)
    

