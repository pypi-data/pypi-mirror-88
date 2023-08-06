#!/usr/bin/env python3

# Standard libraries
from argparse import ArgumentParser, RawTextHelpFormatter
from sys import exit

# Components
from .executor import Executor
from .features.actions import ActionsFeature
from .package.bundle import Bundle
from .package.version import Version
from .system.platform import Platform
from .types.commands import Commands

# Main
def main():

    # Variables
    result = False

    # Arguments creation
    parser = ArgumentParser(
        prog=Bundle.NAME,
        description='%s: Automate interactive CLI tools actions' % (Bundle.NAME),
        add_help=False, formatter_class=RawTextHelpFormatter)

    # Arguments internal definitions
    parser.add_argument('-h', '--help', dest='help', action='store_true',
                        help='Show this help message')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='Show the current version')

    # Arguments optional definitions
    parser.add_argument(
        '--delay-init', dest='delay_init', type=float, default=Executor.DELAY_INIT,
        help='Delay the initial action execution (in s, default: %(default)s)',
        metavar='SECS')
    parser.add_argument(
        '--delay-press', dest='delay_press', type=float, default=Executor.DELAY_PRESS,
        help='Delay the press actions execution (in s, default: %(default)s)',
        metavar='SECS')
    parser.add_argument(
        '--host', dest='host', action='store', default=Executor.LABEL_HOST,
        help='Configure the host name (default: %(default)s' + ', env: ' +
        Bundle.ENV_HOST + ')')
    parser.add_argument(
        '--tool', dest='tool', action='store', default=Executor.LABEL_TOOL,
        help='Configure the tool name (default: %(default)s' + ', env: ' +
        Bundle.ENV_TOOL + ')')
    parser.add_argument('--workdir', dest='workdir', action='store',
                        help='Use a specific working directory path')
    parser.add_argument('--up', dest='actions', action='append_const',
                        const=ActionsFeature.ActionKey(Executor.KEY_UP),
                        help='Press the <UP> key')
    parser.add_argument('--down', dest='actions', action='append_const',
                        const=ActionsFeature.ActionKey(Executor.KEY_DOWN),
                        help='Press the <DOWN> key')
    parser.add_argument('--left', dest='actions', action='append_const',
                        const=ActionsFeature.ActionKey(Executor.KEY_LEFT),
                        help='Press the <LEFT> key')
    parser.add_argument('--right', dest='actions', action='append_const',
                        const=ActionsFeature.ActionKey(Executor.KEY_RIGHT),
                        help='Press the <RIGHT> key')
    parser.add_argument('--enter', dest='actions', action='append_const',
                        const=ActionsFeature.ActionKey(Executor.KEY_ENTER),
                        help='Press the <ENTER> key')
    parser.add_argument('--space', dest='actions', action='append_const',
                        const=ActionsFeature.ActionKey(Executor.KEY_SPACE),
                        help='Press the <SPACE> key')
    parser.add_argument('--press', dest='actions', action='append',
                        type=ActionsFeature.ActionKey, help='Press the specified <KEY>',
                        metavar='KEY')
    parser.add_argument('--ctrl', dest='actions', action='append',
                        type=ActionsFeature.ActionKeyControl,
                        help='Press the specified Ctrl+<KEY>', metavar='KEY')
    parser.add_argument('--read', dest='actions', action='append_const',
                        const=ActionsFeature.ActionRead(),
                        help='Read the buffered data output (forced)')
    parser.add_argument(
        '--wait', dest='actions', action='append', type=ActionsFeature.ActionWait,
        help='Wait the specified time (in s, example: 1.0)', metavar='SECS')
    parser.add_argument('--finish', dest='actions', action='append_const',
                        const=ActionsFeature.ActionFinish(),
                        help='Finish the execution (forced)')

    # Arguments positional definitions
    parser.add_argument('command', nargs='*',
                        help='Command arguments to execute (use -- to separate)')

    # Arguments parser
    options = parser.parse_args()

    # Version informations
    if options.version:
        print('%s %s from %s (python %s)' %
              (Bundle.NAME, Version.get(), Version.path(), Version.python()))
        Platform.flush()
        exit(0)

    # Help informations
    if options.help:
        print(' ')
        parser.print_help()
        print(' ')
        Platform.flush()
        exit(0)

    # Prepare command
    command = str(Commands(options.command))

    # Action executor
    result = ActionsFeature(command, options).run()

    # Result
    if result:
        exit(0)
    else:
        exit(1)

# Entrypoint
if __name__ == '__main__': # pragma: no cover
    main()
