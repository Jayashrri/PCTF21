#!/usr/bin/python3
from .actions import Actions
from os.path import dirname, realpath, join
from stringcolor import cs
from signal import signal, SIGINT
from json import load
import re
import shlex
import sys

class Verification:

    def verify_username(self, username) -> None:
        pattern = r'^[a-zA-Z0-9_ ]{4,}$'
        if not re.match(pattern, username):
            raise Exception('INCORRECT USERNAME FORMAT.')

    def verify_email(self, email) -> None:
        pattern = r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9]+\.[a-zA-Z]+$'
        if not re.match(pattern, email):
            raise Exception('INCORRECT EMAIL FORMAT.')

    def verify_password(self, password) -> None:
        if not len(password) > 4:
            raise Exception('INCORRECT PASSWORD FORMAT.')

    def verify_icecream(self, icecream) -> bool:
        pattern = r'^[a-f0-9]{64}$'
        return bool(re.match(pattern, icecream))

    def verify_cmd(self, cmd) -> (str, list):
        args = shlex.split(cmd)
        try:
            action = args[0].lower()
            assert action in ('signup', 'signin', 'signout', 'exit')

            if action == 'signup':
                assert len(args) == 4
                args[1] = args[1].strip()[:20]
                self.verify_username(args[1])
                self.verify_email(args[2])
                self.verify_password(args[3])

            elif action == 'signin':
                assert len(args) == 3
                args[1] = args[1].strip()[:20]
                self.verify_username(args[1])
                self.verify_password(args[2])

            return action, args[1:]

        except (IndexError, AssertionError):
            raise Exception('INCORRECT COMMAND FORMAT.')

class Shell(Verification):

    def __init__(self, config_file, guide_file):
        config_data = load(open(config_file, 'r'))
        try:
            self.actions = Actions(config_data)
            signal(SIGINT, self.actions.close)
            print(cs(open(guide_file, 'r').read(), "#41fdfe").bold())

        except Exception as e:
            print(cs(str(e), "#ff0000").bold())
            sys.exit(0)

    def prompter(self):
        prompt = cs('\nroot@p_ctf', "#66ff00").bold()
        prompt += cs(':', "#ffffff").bold()
        prompt += cs('~', "#004eff").bold()
        prompt += cs('#  ', "#ff0000").bold()
        return prompt

    def shower_sprinkles(self) -> str:
        prompt = cs('\nHow was your icecream?  ', "#66ff00").bold()
        icecream = input(prompt).strip().lower()

        if not self.verify_icecream(icecream):
            return 'This icecream ain\'t ours.'

        sprinkles = self.actions.fetch_sprinkles(icecream)
        if not sprinkles:
            return 'This icecream ain\'t ours.'

        return 'It will taste even better with these sprinkles on top.\n\n' + sprinkles

    def run(self) -> None:
        try:
            prompt = self.prompter()
            action = 'init'

            while not action == 'exit':
                try:
                    action, args = self.verify_cmd(input(prompt))

                    if action == 'signup':
                        print(self.actions.signup(args))

                    elif action == 'signin':
                        isadmin, response = self.actions.signin(args)
                        print(response)

                        if isadmin:
                            print(self.shower_sprinkles())

                    elif action == 'signout':
                        print(self.actions.signout())

                except Exception as e:
                    print(cs(str(e), "#ff0000").bold())

            self.actions.delete_table()
            print(cs("BYE!", "#66ff00").bold())

        except Exception as e:
            print(cs(str(e), "#ff0000").bold())
