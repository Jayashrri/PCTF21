#!/usr/bin/python3
from os.path import dirname, realpath, join
from stringcolor import cs
from os import system
import requests
import json
import sys

class Shell:

    def __init__(self, config_file, guide_file):
        config = json.load(open(config_file, 'r'))
        self.username = config['username']
        self.host = config['host']
        self.port = config['port']
        print(cs(open(guide_file, 'r').read(), "#41fdfe").bold())

    def get_cipher(self) -> str:
        r = requests.get(f'http://{self.host}:{self.port}/cipher')
        if not r.status_code == 200:
            raise Exception(r.text)
        return r.text

    def exec_shell(self) -> int:
        return system(f'sudo su - {self.username}')

    def prompter(self):
        prompt = cs('\naction', "#66ff00").bold()
        prompt += cs(': ', "#ffffff").bold()
        return prompt

    def run(self) -> None:
        prompt = self.prompter()
        action = 'init'

        while not action == 'exit':
            action = input(prompt)
            try:
                if action == 'flag':
                    print(self.get_cipher())

                elif action == 'shell':
                    exit_code = self.exec_shell()
                    break

                elif not action == 'exit':
                    print('unknown action')

            except Exception as e:
                print(cs(str(e), "#ff0000").bold())

        sys.exit(0)

def main():
    cwd = dirname(realpath(__file__))
    config_file = join(cwd, 'config.json')
    guide_file = join(cwd, 'guidelines.txt')
    shell = Shell(config_file, guide_file)
    shell.run()

if __name__ == '__main__':
    main()
