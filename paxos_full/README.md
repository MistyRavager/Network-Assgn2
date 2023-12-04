This folder contains our implementation of the complete Paxos algorithm, as described in the paper
"Paxos Made Moderately Complex" by Robbert van Renesse and Deniz Altinbuken.

Note that this implementation is not complete due to time constraints. We have implemented all of
the functionality described in the paper, but did not have the time to test and debug it. As such,
it is currently non-functional.

### Files

- `acceptor.py`: The `Acceptor` class.
- `leader.py`: The `Leader` class. This class also implements the Scout and Commander roles.
- `replica.py`: The `Replica` class.
- `client.py`: The `Client` class, which represents an external client that wishes to submit a
  request to the state machine.
- `client_node.py`: A simple script to run a client node.
- `mn_test.py`: mininet test script, should be run once per node:
  - `python mn_test.py <hostno>`
  - `hostno` should be an integer between 0 and 4, inclusive.
  - This script creates a replica, acceptor, and leader on the specified host.
- `dir.py`: The directory, stores the IP addresses and ports of all nodes in the system.
- `classes.py`: Helper classes to represent the various messages sent.
