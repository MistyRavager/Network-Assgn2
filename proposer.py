# this is the proposer in the paxos algorithm

import json
import socket
import sys

from typing import Tuple

hosts = [
    # ('localhost', 9995),
    # ('localhost', 9996),
    # ('localhost', 9997),
    # ('localhost', 9998),
    ('localhost', 9999)
]

def get_promises(proposal_number: int, host_list: list) -> Tuple[int, int] | None:
    global hosts

    N_max, v_max = -1, 0

    for i in host_list:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(hosts[i])

        msg = {'type':'promise', 'proposal_number':proposal_number}
        sock.send(json.dumps(msg).encode('ascii'))

        res_msg = sock.recv(1024).decode('ascii')
        res_msg = json.loads(res_msg)
        sock.close()
        print(f"Got promise {res_msg}")
        if res_msg['type'] == 'reject':
            return None
        assert res_msg['type'] == 'promise'
        if 'proposal_number' in res_msg and res_msg['proposal_number'] > N_max:
            N_max, v_max = res_msg['proposal_number'], res_msg['value']

    return N_max, v_max

def send_commits(proposal_number: int, value: int, host_list: list) -> bool:
    global hosts

    for i in host_list:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(hosts[i])

        msg = {'type':'commit', 'proposal_number':proposal_number, 'value':value}
        sock.send(json.dumps(msg).encode('ascii'))

        res_msg = sock.recv(1024).decode('ascii')
        res_msg = json.loads(res_msg)
        print(f"Got response {res_msg}")
        sock.close()
        if res_msg['type'] == 'reject':
            return False

    return True

def try_propose(proposal_number: int, value: int):
    global hosts, ports

    promise = get_promises(proposal_number, list(range(len(hosts))))

    if promise is None:
        return False

    N_max, v_max = promise

    if N_max > -1:
        print(f"Using value {v_max} from proposal {N_max}")
        value = v_max

    return send_commits(proposal_number, value, list(range(len(hosts))))

if __name__ == '__main__':
    # python3 proposer.py proposal_number value
    proposal_number = int(sys.argv[1])
    value = int(sys.argv[2])
    if try_propose(proposal_number, value):
        print('Proposed successfully')
    else:
        print('Proposed failed')
