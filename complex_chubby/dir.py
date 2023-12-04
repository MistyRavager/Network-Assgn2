import os

if os.environ.get('LOCAL'):
    chubbies = [
        ('localhost', 4001),
        ('localhost', 4002),
        ('localhost', 4003),
        ('localhost', 4004),
        ('localhost', 4005),
    ]
else:
    chubbies = [
        ('10.0.0.1', 4000),
        ('10.0.0.2', 4000),
        ('10.0.0.3', 4000),
        ('10.0.0.4', 4000),
        ('10.0.0.5', 4000),
    ]