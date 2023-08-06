#!/usr/bin/env python3

# Components
from ..executor import Executor

# ActionsFeature class
class ActionsFeature:

    # Members
    __actions = []
    __executor = None
    __result = False

    # Key action class
    class ActionKey:
        def __init__(self, key):
            self.key = str(key)

    # Key action class
    class ActionKeyControl:
        def __init__(self, key):
            self.key = str(key)

    # Finish action class
    class ActionFinish:
        def __init__(self):
            self.finish = True

    # Read action class
    class ActionRead:
        def __init__(self):
            self.read = True

    # Wait action class
    class ActionWait:
        def __init__(self, wait):
            self.wait = float(wait)

    # Constructor
    def __init__(self, command, options):

        # Store actions
        self.__actions = options.actions

        # Configure executor
        Executor.configure(host=options.host, tool=options.tool)

        # Create executor
        try:
            self.__result = False
            self.__executor = Executor(command=command, delay_init=options.delay_init,
                                       delay_press=options.delay_press,
                                       workdir=options.workdir)

        # Intercept interruptions
        except KeyboardInterrupt:
            self.finish()

    # Finish
    def finish(self, force=False):

        # Finish executor
        if self.__executor:
            self.__result = self.__executor.finish(force=force) == 0
            self.__executor = None

    # Run
    def run(self):

        # Wrap executor
        try:

            # Interact with executor
            for index, action in enumerate(self.__actions if self.__actions else []):

                # Key actions
                if isinstance(action, ActionsFeature.ActionKey):
                    self.__executor.press(action.key)

                # Ctrl+key actions
                if isinstance(action, ActionsFeature.ActionKeyControl):
                    self.__executor.press(action.key, control=True)

                # Read actions
                elif isinstance(action, ActionsFeature.ActionRead):
                    self.__executor.read()
                    break

                # Wait actions
                elif isinstance(action, ActionsFeature.ActionWait):
                    self.__executor.wait(action.wait)

                # Finish actions
                elif isinstance(action, ActionsFeature.ActionFinish):
                    self.finish(force=True)
                    break

                # Read outputs
                next_finish = index + 1 < len(self.__actions) and isinstance(
                    self.__actions[index + 1], ActionsFeature.ActionFinish)
                if not next_finish:
                    self.__executor.read()

        # Catch interruptions
        except KeyboardInterrupt:
            pass

        # Finish executor
        self.finish()

        # Result
        return self.__result
