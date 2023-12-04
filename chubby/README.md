A simple lock service, inspired by the Chubby algorithm used by Google.

The Chubby algorithm uses the Paxos algorithm to achieve consensus. However, since we were unable
to complete the Paxos algorithm in time, this implementation simply uses a single server to handle
all requests.

### Files

- `server.py`: The server implementation.
- `client.py`: The client implementation.
- `server_node.py`: Runs a server node.
- `client_node.py`: Runs a client node.
- `web_demo.py`, `templates/index.html`: Runs a small web demo, that shows the status of acquired locks.
