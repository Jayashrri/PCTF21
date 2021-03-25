from flask import Flask, request
from os.path import dirname, realpath, join
from modules.algorithm import encrypt
from modules.game import xor, solve
import requests
import json

app = Flask(__name__)

@app.route('/cipher', methods=['GET'])
def server():
    host = app.config['host']
    port = app.config['request_port']

    r = requests.get(f'http://{host}:{port}/cipher')
    if not r.status_code == 200:
        return 'an unexpected error occured', 500
    
    pt = bytes.fromhex(r.text)
    key = bytes.fromhex(app.config['key'])
    return encrypt(pt, key).hex(), 200

@app.route('/encrypted_keys', methods=['GET'])
def encrypted_keys():
    lvl3_key = request.get_json()['key']
    lvl2_key = app.config['key']
    message = f'level-2 key: {lvl2_key}\nlevel-3 key: {lvl3_key}'.encode()
    key = solve(app.config['keywords'], 1337)
    return xor(message, key).hex(), 200

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'healthy', 200

def main():
    cwd = dirname(realpath(__file__))
    config_file = join(cwd, 'config.json')
    config = json.load(open(config_file, 'r'))

    port = config['listen_port']
    app.config['host'] = host = config['host']
    app.config['request_port'] = config['request_port']
    app.config['key'] = config['key']
    app.config['keywords'] = config['keywords']

    app.run(host=host, port=port, debug=True, use_reloader=True)

if __name__ == '__main__':
    main()
