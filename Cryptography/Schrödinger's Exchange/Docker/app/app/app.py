#!/usr/local/bin/python3
from flask import Flask
from blueprints.qkd import key_distribution_blueprint
from blueprints.utils import utils_blueprint
from modules.actions import Actions
from modules.bb84 import BB84
from os.path import dirname, realpath, join
from json import load
import logging

def create_logger():
    cwd = dirname(realpath(__file__))
    log_file = join(cwd, 'logs.txt')

    logger = logging.getLogger()
    log_formatter = logging.Formatter("*"*30 + "\n%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d\n")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)
    file_handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    return logger

def main():
    logger = create_logger()

    try:
        cwd = dirname(realpath(__file__))
        config_file = join(cwd, 'config.json')
        data = load(open(config_file, 'r'))

        app = Flask(__name__)
        app.register_blueprint(key_distribution_blueprint)
        app.register_blueprint(utils_blueprint)

        app.config['db'] = Actions(data['db'], logger)
        app.config['BB84'] = BB84()
        app.config['flag'] = data['app']['flag']
        app.config['image_url'] = data['app']['image_url']
        app.config['ssh_password'] = data['app']['ssh_password']
        app.config['logger'] = logger

        host = data['app']['host']
        port = data['app']['port']

        app.run(host=host, port=port, debug=True, use_reloader=True)
    except Exception as e:
        logger.exception(str(e))

if __name__ == '__main__':
    main()
