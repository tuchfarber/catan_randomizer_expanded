from flask import Flask, request, jsonify
from gevent.wsgi import WSGIServer
from board import Board

app = Flask(__name__, static_url_path='')

@app.route('/', methods=['GET'])
def index():
    '''Returns client page'''
    return app.send_static_file('index.html')

@app.route('/api/generate/random', methods=['GET'])
def generate_random():
    random_board = Board(4)
    return jsonify(random_board.to_dict())

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()