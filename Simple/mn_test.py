from node import Node
import threading
import sys

node = Node(sys.argv[1], 5, [1, 2, 3, 4, 5], 5, randomize_acceptors=True, wait_time=0.5)
threading.Thread(target=node.listen).start()
node.propose(sys.argv[2])
