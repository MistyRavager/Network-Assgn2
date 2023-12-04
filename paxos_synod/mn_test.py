from node import Node
import threading
# import time
from socket import *
import os
import sys

node = Node(int(sys.argv[1]), 5, list(range(4)), 5, randomize_acceptors=True, wait_time=0.5)
# send_sock = socket(AF_INET, SOCK_DGRAM)
# recv_sock = socket(AF_INET, SOCK_DGRAM)
# recv_sock.bind((node.hostname, 1234))

# for i in range(1, 4):
#     if i != int(sys.argv[1]):
#         send_sock.sendto('hey'.encode(), (node.hostname, 1234))
        # while os.system('ping -c 1 ' + stub + str(i)) == 0:
        #     pass

threading.Thread(target=node.listen).start()
# time.sleep(10)
# stub = '10.0.0.'
# for i in range(1, 4):
#     if i != int(sys.argv[1]):
#         # node.send_message(stub + str(i), 5000, 'prepare', 0)
#         while os.system('ping -c 1 ' + stub + str(i)) == 0:
#             pass
def props():
    res = node.propose(int(input('Whatchu want?')))
    print(res)

threading.Thread(target=props).start()
