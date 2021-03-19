from flask import Flask
from stringcolor import cs
from os.path import dirname, realpath, join
from modules.algorithm import encrypt
import requests
import json

app = Flask(__name__)

@app.route('/cipher', methods=['GET'])
def server():
    host = app.config['host']
    port = app.config['port']

    r = requests.get(f'http://{host}:{port}/cipher')
    if not r.status_code == 200:
        return 'an unexpected error occured', 500
    
    pt = bytes.fromhex(r.text)
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
    port = config['l_port']
    app.config['host'] = host
    app.config['port'] = config['r_port']
    app.config['key'] = config['key']

    app.run(host=host, port=port, debug=True, use_reloader=True)

if __name__ == '__main__':
    main()
