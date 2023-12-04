This folder contains our implementation of the Synod algorithm, which is a distributed algorithm
for solving the consensus problem in a network of unreliable processes.

This is a complete implementation of the paper "Paxos Made Simple" by Leslie Lamport, including a
recreation of the livelock scenario described in the paper. We have also implemented the
randomization and backoff optimizations described in the paper.

### Files

- `proposer.py`: The proposer process.
- `acceptor.py`: The acceptor process.
- `message.py`: The message classes.
- `node.py`: Defines a Node class containing a proposer and an acceptor
- `dir.py`: Directory, which stores the IP addresses and ports of all the nodes in the network.
- `mn_test.py`: A test script to be run within mininet:
  ```
  python3 mn_test.py <proposer_number>
  ```
  Should be run once for each node (h0 to h4) in the network.
- `test.py`, `expobackoff.py`, `randomize.py`: Various test scripts, which show the livelock
  scenario and the optimizations.
