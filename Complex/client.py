"""
    The following code defines a class for the clients in a Complex
    Paxos driven network. The clients are the nodes that send requests
    to the replicas.
"""

# Importing libraries
import json
from socket import *
import threading
import dataclasses
import random
import string

# Importing files
from classes import *
from dir import *

# Class Definition
class Client:
    def __init__(self, id):
        """
            The constructor for the Client class. It is responsible for
            initializing the client object with the given parameters.
            id:
                The id of the client instance - associated with host and
                port number.
            replicas:
                The list of replicas associated with the client instance.
                To be initialized!
        """

        # Main Paramaters
        self.id = id
        self.replicas = list(range(0, len(replicas)))
        self.count = 0

    # Issue a new request
    def issue_request(self, op_val):
        """
            This function is responsible for issuing a new request to the
            replicas.
        """

        # Create a new command
        command = Command(self.id, self.count, op_val)
        self.count += 1

        # Create a new request
        request = Request(command)
        return request
    
    # Listen for responses
    def listen(self):
        ipp = clients[self.id]
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(ipp)

        while True:
            data, addr = sock.recvfrom(1024)
            response = json.loads(data.decode('ascii'))
            response = Response.from_json(response)
            print("Client", self.id, "received response:", response.result)

            # Generate 10 char random string/ lock service
            op_val = ''.join(random.choice(string.ascii_letters) for i in range(10))

            # Issue a new request ??
            request = self.issue_request(op_val)

            # Send request to replicas
            for i in self.replicas:
                sock.sendto(request.to_json().encode('ascii'), replicas[i])


        