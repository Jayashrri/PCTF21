from flask import Flask
from os.path import dirname, realpath, join
from modules.algorithm import encrypt
from os import urandom
from random import randint
import json

app = Flask(__name__)

@app.route('/cipher', methods=['GET'])
def server():
    offset = randint(8, 24)
    pt = urandom(offset) + app.config['flag'].encode() + urandom(32-offset)
    key = bytes.fromhex(app.config['key'])
    return encrypt(pt, key).hex(), 200

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'healthy', 200

def main():
    cwd = dirname(realpath(__file__))
    config_file = join(cwd, 'config.json')
    config = json.load(open(config_file, 'r'))

    host = config['host']
    port = config['port']
    app.config['flag'] = config['flag']
    app.config['key'] = config['key']

    app.run(host=host, port=port, debug=True, use_reloader=True)

if __name__ == '__main__':
    main()
