#!/usr/local/bin/python3
from flask import Flask
from blueprints.qkd import key_distribution_blueprint
from blueprints.utils import utils_blueprint
from modules.actions import Actions
from modules.bb84 import BB84
from os.path import dirname, realpath, join
from json import load

def main():

    try:
        cwd = dirname(realpath(__file__))
        config_file = join(cwd, 'config.json')
        data = load(open(config_file, 'r'))

        app = Flask(__name__)
        app.register_blueprint(key_distribution_blueprint)
        app.register_blueprint(utils_blueprint)

        app.config['db'] = Actions(data['db'])
        app.config['BB84'] = BB84()
        app.config['flag'] = data['app']['flag']
        app.config['image_url'] = data['app']['image_url']
        app.config['ssh_password'] = data['app']['ssh_password']
        app.config['ssh_port'] = data['app']['ssh_port']

        host = data['app']['host']
        port = data['app']['port']

        app.run(host=host, port=port, debug=True, use_reloader=True)
    except Exception as e:
        pass

if __name__ == '__main__':
    main()
