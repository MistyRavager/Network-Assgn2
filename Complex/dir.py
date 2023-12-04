import os

local = True

if os.environ.get('LOCAL'):
    replicas = [
        ("localhost", 5000),
        ("localhost", 5001),
        ("localhost", 5002),
        ("localhost", 5003),
        ("localhost", 5004),
    ]

    leaders = [
        ("localhost", 6000),
        ("localhost", 6001),
        ("localhost", 6002),
        ("localhost", 6003),
        ("localhost", 6004),
    ]

    acceptors = [
        ("localhost", 7000),
        ("localhost", 7001),
        ("localhost", 7002),
        ("localhost", 7003),
        ("localhost", 7004),
    ]
else:
    replicas = [
        ("10.0.0.100", 5000),
        ("10.0.0.101", 5000),
        ("10.0.0.102", 5000),
        ("10.0.0.103", 5000),
        ("10.0.0.104", 5000),
    ]

    leaders = [
        ("10.0.0.110", 6000),
        ("10.0.0.111", 6000),
        ("10.0.0.112", 6000),
        ("10.0.0.113", 6000),
        ("10.0.0.114", 6000),
    ]
    
    acceptors = [
        ("10.0.0.120", 7000),
        ("10.0.0.121", 7000),
        ("10.0.0.122", 7000),
        ("10.0.0.123", 7000),
        ("10.0.0.124", 7000),
    ]
