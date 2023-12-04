# If all test work, delete this.

# class Message:
#     """
#     Superclass of all messages.
#     """
#     def __init__(self, recvr_id, sender_id, ballot_num, msg_type) -> None:
#         self.sender_id = sender_id
#         self.recvr_id = recvr_id
#         self.ballot_num = ballot_num
#         self.msg_type = msg_type


# class Prepare(Message):
#     """
#     Phase 1a
#     """
#     def __init__(self, recvr_id, sender_id, ballot_num) -> None:
#         super().__init__(recvr_id, sender_id, ballot_num, 'prepare')


# class Promise(Message):
#     """
#     Phase 1b.
#     """
#     def __init__(self, recvr_id, sender_id, ballot_num, acc) -> None:
#         super().__init__(recvr_id, sender_id, ballot_num, 'promise')
#         self.acc = acc


# class AcceptRequest(Message):
#     """
#     Phase 2a.
#     """
#     def __init__(self, recvr_id, sender_id, ballot_num, slot, command) -> None:
#         super().__init__(recvr_id, sender_id, ballot_num, 'accept-request')
#         self.slot = slot
#         self.command = command

# class Ack(Message):
#     """
#     Phase 2b.
#     """
#     def __init__(self, recvr_id, sender_id, ballot_num) -> None:
#         super().__init__(recvr_id, sender_id, ballot_num, 'ack')