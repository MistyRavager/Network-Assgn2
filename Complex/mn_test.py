import threading
from replica import Replica
from acceptor import Acceptor
from leader import Leader
from dir import *
import sys

replica = Replica(int(sys.argv[1]))
leader = Leader(int(sys.argv[2]))
acceptor = Acceptor(int(sys.argv[3]))

replica_thread = threading.Thread(target=replica.listen).start()
leader_thread = threading.Thread(target=leader.listen).start()
acceptor_thread = threading.Thread(target=acceptor.listen).start()

