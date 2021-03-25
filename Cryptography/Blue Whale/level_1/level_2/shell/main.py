#!/usr/bin/python3
from os.path import dirname, realpath, join
from stringcolor import cs
from os import system
from hashlib import md5
import json
import sys

class Shell:

    def __init__(self, config_file, guide_file):
        config = json.load(open(config_file, 'r'))
        self.username = config['username']
        self.keywords = config['keywords']
        print(cs(open(guide_file, 'r').read(), "#41fdfe").bold())

    def exec_shell(self) -> int:
        return system(f'sudo su - {self.username}')

    def play(self, keywords: list) -> list:
        return [md5(k.encode()).digest().hex() for k in keywords]

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
                if action == 'play':
                    print("Here, have some toys:")
                    for toy in self.play(self.keywords):
                        print(toy)

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
