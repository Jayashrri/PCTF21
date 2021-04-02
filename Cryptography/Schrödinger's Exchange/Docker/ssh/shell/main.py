#!/usr/bin/python3
from os.path import dirname, realpath, join
from modules.shell import Shell

def main():
    cwd = dirname(realpath(__file__))
    config_file = join(cwd, 'config.json')
    guide_file = join(cwd, 'guidelines.txt')

    shell = Shell(config_file, guide_file)
    shell.run()

if __name__ == '__main__':
    main()
