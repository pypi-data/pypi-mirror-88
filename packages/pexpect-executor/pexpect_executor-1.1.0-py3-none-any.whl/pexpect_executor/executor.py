#!/usr/bin/env python3

# Standard libraries
from errno import ENOENT
from getpass import getuser
from os import chdir, environ
from time import sleep

# Modules libraries
from pexpect import EOF, spawn, TIMEOUT

# Components
from .package.bundle import Bundle
from .prints.colors import Colors

# Executor
class Executor:

    # Constants
    KEY_UP = '\033[A'
    KEY_DOWN = '\033[B'
    KEY_LEFT = '\033[D'
    KEY_RIGHT = '\033[C'
    KEY_ENTER = '\r'
    KEY_SPACE = ' '

    # Delays
    DELAY_INIT = 1.0
    DELAY_PRESS = 0.5
    DELAY_PROMPT = 1.0

    # Labels
    LABEL_HOST = 'preview'
    LABEL_TOOL = 'executor'

    # Members
    __child = None
    __delay_init = None
    __delay_press = None
    __delay_prompt = None
    __host = environ[Bundle.ENV_HOST] if Bundle.ENV_HOST in environ else LABEL_HOST
    __tool = environ[Bundle.ENV_TOOL] if Bundle.ENV_TOOL in environ else LABEL_TOOL

    # Constructor
    def __init__(self, command, delay_init=DELAY_INIT, delay_press=DELAY_PRESS,
                 delay_prompt=DELAY_PROMPT, workdir=None):

        # Prepare delays
        self.__delay_init = float(delay_init)
        self.__delay_press = float(delay_press)
        self.__delay_prompt = float(delay_prompt)

        # Prepare workdir
        if workdir:
            self.__prompt('cd %s' % workdir)
            chdir(workdir)

        # Prepare command
        self.__prompt(command)
        if command:
            self.__child = spawn('/bin/sh', ['-c', command])

            # Delay executor initialization
            if self.__delay_init > 0.0:
                Executor.sleep(self.__delay_init)
                self.read()

    # Configure
    @staticmethod
    def configure(host=LABEL_HOST, tool=LABEL_TOOL):

        # Prepare host
        Executor.__host = host

        # Prepare tool
        Executor.__tool = tool

    # Prompt
    def __prompt(self, command):

        # Display prompt
        print(
            '%s%s%s@%s%s%s:%s~/%s%s$ ' %
            (Colors.GREEN_THIN, getuser(), Colors.RESET, Colors.RED_THIN, self.__host,
             Colors.RESET, Colors.YELLOW_THIN, self.__tool, Colors.RESET), end='',
            flush=True)

        # Delay prompt
        Executor.sleep(self.__delay_prompt)

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
    def press(self, key, control=False):

        # Execution check
        if not self.__child:
            return self

        # Delay press
        Executor.sleep(self.__delay_press)

        # Press Ctrl+key
        if control:
            self.__child.sendcontrol(key)

        # Press Ctrl+key
        else:
            self.__child.send(key)

        # Result
        return self

    # Read
    def read(self):

        # Execution check
        if not self.__child:
            return self

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
    def finish(self, force=False):

        # Execution check
        if not self.__child:
            return ENOENT

        # Read and wait execution
        if not force:
            while self.__child.isalive():
                self.read()

        # Finish execution
        self.__child.terminate(force=force)

        # Result
        return self.__child.exitstatus

    # Sleep
    @staticmethod
    def sleep(delay):

        # Delay execution
        sleep(delay)
