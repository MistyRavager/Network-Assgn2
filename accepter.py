# This is code for the accepter process in the Paxos algorithm

import socket
import os
import time
import random
import json
import threading

N_promised = 0 # The highest proposal number proposed to this accepter
N_acc = 0 # The highest proposal number accepted by this accepter
v_acc = 0

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

port = 9999

# Bind to the port
serversocket.bind((host, port))

# Start listening on the port
serversocket.listen(5)

def process(clientsocket, addr):
    global N_promised, N_acc, v_acc
    msg = clientsocket.recv(1024)
    msg = msg.decode('ascii')
    msg = json.loads(msg)
    res_msg = None

    type, N_proposed = msg['type'], msg['proposal_number']
    if N_proposed < N_promised:
        res_msg = {'type':'reject'}
        clientsocket.send(res_msg.encode('ascii'))
        return
    
    if type == 'prepare':
        if N_acc > 0:
            res_msg = {'type':'promise', 'proposal_number':N_acc, 'value':v_acc}
        else:
            res_msg = {'type':'promise'}
        
        N_promised = N_proposed
    elif type == 'commit':
        if not 'value' in msg:
            res_msg = {'type':'reject'}
            clientsocket.send(res_msg.encode('ascii'))
            return
        if N_proposed != N_promised:
            res_msg = {'type':'reject'}
            clientsocket.send(res_msg.encode('ascii'))
            return
        N_acc, v_acc = N_proposed, msg['value']
        res_msg = {'type':'ack'}

    clientsocket.send(res_msg.encode('ascii'))

while True:
    clientsocket,addr = serversocket.accept()

    threading.Thread(target=process, args=(clientsocket, addr)).start()

serversocket.close()
    
