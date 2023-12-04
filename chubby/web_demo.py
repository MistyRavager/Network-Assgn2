from flask import Flask, request, jsonify, render_template
import uuid
import sys
from simple_chubby.client_node import *
from simple_chubby.client import Client

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())


# dictionary of client_id: id
d = {}

id = int(sys.argv[1])
client = Client(server_port, server_host, id, 3)



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', id=id, locks=list(locks), acqu_locks=list(acqu_locks))


@app.route('/acquire', methods=['POST'])
def acquire():
    # get client id from request body
    lock = int(request.get_json()['lock'])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    threading.Thread(target=get_lock, args=(s, lock, client)).start()
    return jsonify({'id': id})
      

if __name__ == '__main__':
    app.run(host='localhost', port=8080+id, debug=True)

