class Message:
    def __init__(self, sender_id, recvr_id, ballot_num, msg_type) -> None:
        self.sender_id = sender_id
        self.recvr_id = recvr_id
        self.ballot_num = ballot_num
        self.msg_type = msg_type


class Prepare(Message):
    def __init__(self, sender_id, recvr_id, ballot_num) -> None:
        super().__init__(sender_id, recvr_id, ballot_num, 'prepare')


class Promise(Message):
    def __init__(self, sender_id, recvr_id, ballot_num, result, acc_num=None, acc_val=None) -> None:
        super().__init__(sender_id, recvr_id, ballot_num, 'promise')
        self.acc_num = acc_num
        self.acc_val = acc_val


class AcceptRequest(Message):
    def __init__(self, sender_id, recvr_id, ballot_num, slot, command) -> None:
        super().__init__(sender_id, recvr_id, ballot_num, 'accept-request')
        self.slot = slot
        self.command = command

# TODO: What exactly are the cases for this?
class Ack(Message):
    def __init__(self, sender_id, recvr_id, ballot_num) -> None:
        super().__init__(sender_id, recvr_id, ballot_num, 'ack')