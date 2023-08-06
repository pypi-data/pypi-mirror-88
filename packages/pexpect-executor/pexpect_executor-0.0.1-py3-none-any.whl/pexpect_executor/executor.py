#!/usr/bin/env python3

# Standard libraries
from getpass import getuser
from os import chdir
from time import sleep

# Modules libraries
from pexpect import EOF, spawn, TIMEOUT

# Executor
class Executor:

    # Constants
    KEY_UP = '\033[A'
    KEY_DOWN = '\033[B'
    KEY_ENTER = '\r'
    KEY_SPACE = ' '

    # Attributes
    host = 'preview'
    tool = 'executor'

    # Members
    __child = None

    # Constructor
    def __init__(self, command, workdir=None):

        # Prepare workdir
        if workdir:
            self.__prompt('cd %s' % workdir)
            chdir(workdir)

        # Prepare command
        self.__prompt(command)
        if command:
            self.__child = spawn('/bin/sh', ['-c', command])

    # Configure
    @staticmethod
    def configure(host, tool):

        # Prepare host
        Executor.host = host

        # Prepare tool
        Executor.tool = tool

    # Prompt
    def __prompt(self, command):

        # Display prompt
        print('\033[32m%s@%s \033[33m%s\033[0m $ ' % (getuser(), self.host, self.tool),
              end='', flush=True)

        # Delay prompt
        Executor.sleep(1)

        # Display command
        if command:
            print('%s ' % (command), end='', flush=True)
        else:
            Executor.sleep(10)
            print('', flush=True)

        # Delay command
        Executor.sleep(1)
        print(' ', flush=True)

    # Press
    def press(self, key):

        # Send key
        self.__child.send(key)

        # Result
        return self

    # Read
    def read(self):

        # Read stream
        while True:
            try:
                output = self.__child.read_nonblocking(size=1024, timeout=1)
            except (AttributeError, EOF, KeyboardInterrupt, TIMEOUT):
                output = None
            if not output:
                break
            output = output.decode('utf-8', errors='ignore')
            output = output.replace('\x1b[6n', '')
            print(output, end='', flush=True)

        # Result
        return self

    # Wait
    def wait(self, delay):

        # Delay execution
        Executor.sleep(delay)

        # Result
        return self

    # Finish
    def finish(self):

        # Read and wait execution
        self.read()
        self.wait(1)

        # Result
        return self

    # Sleep
    @staticmethod
    def sleep(delay):

        # Delay execution
        sleep(delay)
