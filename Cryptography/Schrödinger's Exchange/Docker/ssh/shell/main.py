#!/usr/bin/python3
from os.path import dirname, realpath, join
from modules.shell import Shell
import logging

def create_logger():
    cwd = dirname(realpath(__file__))
    log_file = join(cwd, 'logs/shell.log')

    logger = logging.getLogger()
    log_formatter = logging.Formatter("*"*30 + "\n%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d\n")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)
    file_handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    return logger

def main():
    cwd = dirname(realpath(__file__))
    config_file = join(cwd, 'config.json')
    guide_file = join(cwd, 'guidelines.txt')
    logger = create_logger()

    shell = Shell(config_file, guide_file, logger)
    shell.run()

if __name__ == '__main__':
    main()
