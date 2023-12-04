from client import Client
import threading


c = Client(0)
threading.Thread(target=c.listen).start()

while True:
    c.issue_request(input('Whatchu want?'))
