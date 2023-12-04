from typing import List, Dict
from dataclasses import dataclass
import threading
from threading import Lock
import json
import socket
from typing import Tuple

from dir import leaders, acceptors
import classes


@dataclass
class Scout:
    waitfor: List[int]
    pvalues: Dict[int, Tuple[classes.Ballot, classes.Command]]
    ballot: classes.Ballot


@dataclass
class CommanderId:
    slot: int
    command: classes.Command


@dataclass
class CommanderState:
    waitfor: List[int]
    ballot_num: int


class Leader:
    id: int
    active: bool = False
    ballot_num: int = 0
    proposals: Dict[int, classes.Command] = {}
    scout: Scout | None = None
    sock: socket.socket
    lock: Lock
    commanders: Dict[CommanderId, CommanderState] = {}

    def __init__(self, id: int):
        self.id = id
        self.lock = Lock()

    def start_scout(self):
        self.scout = Scout(list(range(len(acceptors))), {},
                           classes.Ballot(self.ballot_num, self.id))
        for i in range(len(acceptors)):
            self.sock.sendto(classes.P1A(classes.MessageType.P1A, i,
                             self.scout.ballot).to_json().encode(), acceptors[i])

    def handle_propose(self, message: classes.Propose):
        with self.lock:
            if message.slot in self.proposals:
                return
            self.proposals[message.slot] = message.command
            if self.active:
                self.start_commander(message.slot, message.command)

    def handle_p1b(self, message: classes.P1B):
        with self.lock:
            if self.scout is None:
                return
            if message.ballot != self.scout.ballot:
                # preempted
                self.active = False
                self.ballot_num = message.ballot.num + 1
                self.start_scout()
            self.scout.waitfor.remove(message.acceptor_id)
            # update self.scout.pvalues from message.accepted
            for (slot, ballot, command) in message.accepted:
                if slot not in self.scout.pvalues or self.scout.pvalues[slot][0] < ballot:
                    self.scout.pvalues[slot] = (ballot, command)

            if len(self.scout.waitfor) <= len(acceptors) // 2:
                # adopted as leader
                # update self.proposals from self.scout.pvalues
                for slot, (ballot, command) in self.scout.pvalues.items():
                    self.proposals[slot] = command

                # spawn commanders
                for slot, command in self.proposals.items():
                    self.start_commander(slot, command)

    def start_commander(self, slot: int, command: classes.Command):
        waitfor = list(range(len(acceptors)))
        commander = CommanderId(slot, command)
        self.commanders[commander] = CommanderState(waitfor, self.ballot_num)
        for i in range(len(acceptors)):
            self.sock.sendto(classes.P2A(classes.MessageType.P2A, i, classes.Ballot(
                self.ballot_num, self.id), slot, command).to_json().encode(), acceptors[i])

    def handle_p2b(self, message: classes.P2B):
        with self.lock:
            commander = CommanderId(message.slot, message.command)
            if commander not in self.commanders:
                return
            state = self.commanders[commander]
            if message.ballot != classes.Ballot(state.ballot_num, self.id):
                # preempted
                self.active = False
                self.ballot_num = message.ballot.num + 1
                self.start_scout()
                return
            state.waitfor.remove(message.acceptor_id)
            if len(state.waitfor) <= len(acceptors) // 2:
                # decided
                del self.commanders[commander]
                for i in range(len(acceptors)):
                    self.sock.sendto(classes.Decision(classes.MessageType.DECISION,
                                                      message.slot, message.command).to_json().encode(), acceptors[i])

    def handle(self, msg: dict):
        # types: propose, p1b, p2b
        if msg["type"] == classes.MessageType.PROPOSE.value:
            self.handle_propose(classes.Propose.from_dict(msg))
        elif msg["type"] == classes.MessageType.P1B.value:
            self.handle_p1b(classes.P1B.from_dict(msg))
        elif msg["type"] == classes.MessageType.P2B.value:
            self.handle_p2b(classes.P2B.from_dict(msg))

    def listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = leaders[self.id][1]
        self.sock.bind(("", ('0.0.0.0', port)))

        with self.lock:
            self.start_scout()

        while True:
            data, addr = self.sock.recvfrom(1024)
            self.handle(json.loads(data.decode()))
