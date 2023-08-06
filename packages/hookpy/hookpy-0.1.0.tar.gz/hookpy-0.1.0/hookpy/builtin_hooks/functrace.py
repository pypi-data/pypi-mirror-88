import functools
import inspect

from hookpy import Hook, compat


class FuncTracePrint(Hook):
    def __init__(self):
        self.impl = None

    def create_impl(self, func_id, func) -> bool:
        isasyncgen = False or (compat.Python3_6AndLater
                               and inspect.isasyncgenfunction(func))
        if not inspect.iscoroutinefunction(func) and not isasyncgen:

            @functools.wraps(func)
            def wrapped(*args, **kw):
                print(func_id)
                return func(*args, **kw)

            self.impl = wrapped
            return True
        return False

    def get_impl(self):
        return self.impl

    def enabled(self) -> bool:
        return True

    def is_enabled(self, enabled: bool):
        return
