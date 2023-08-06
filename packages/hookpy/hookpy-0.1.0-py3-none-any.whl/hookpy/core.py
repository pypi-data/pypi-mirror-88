"""register ast hooks for top-level functions and class member functions, 
make function can be modified during runtime.
"""

import abc
import atexit
import functools
import inspect
import json
import os
import re
import threading
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple, Type, Union

from hookpy import compat, funcid
from hookpy.constants import HOOKPY_CONFIG_PATH, HOOKPY_ENABLE
from hookpy.funcid import try_remove_decorator

_FUNC_ID_TO_HOOKS = {}  # type: Dict[str, List["Hook"]]

_LOCK = threading.Lock()


def read_config(config_path: str):
    config_path = Path(config_path)
    with config_path.open("r") as f:
        data = json.load(f)
    return data


class HookConfig:
    def __init__(self, config_path: Union[Path, str], config):
        self.hook_folders = config.get("folders", [])  # type: List[str]
        self.hook_projects = config.get("projects", [])  # type: List[str]
        self.func_excludes = [
            re.compile(s) for s in config.get("func_excludes", [])
        ]
        self.folder_excludes = [
            re.compile(s) for s in config.get("folder_excludes", [])
        ]

        self.hooks_config = config["hooks"]
        self.config_path = Path(config_path)

        # if dir in hook_folders is relative, use config_path to convert it
        # to absolute
        for i, folder in enumerate(self.hook_folders):
            folder_p = Path(folder)
            if not folder_p.is_absolute():
                folder_p = self.config_path.parent / folder_p
            self.hook_folders[i] = str(folder_p)

    def get_hook_classes(
            self
    ) -> Generator[Tuple[Type["Hook"], Dict[str, Any]], None, None]:
        for hook_cfg in self.hooks_config:
            name = hook_cfg["type"]
            config = hook_cfg.get("config", None)  # type: Dict[str, Any]
            if not config:
                config = {}

            hook_cls = funcid.get_module_object_by_imp_id(name)
            yield (hook_cls, config)


HOOK_CONFIG = None  # type: Optional[HookConfig]


def init_hook_config():
    global HOOK_CONFIG
    if HOOKPY_ENABLE:
        HOOK_CONFIG = HookConfig(HOOKPY_CONFIG_PATH,
                                 read_config(HOOKPY_CONFIG_PATH))


def enable_hook():
    global HOOKPY_ENABLE
    HOOKPY_ENABLE = True


def disable_hook():
    global HOOKPY_ENABLE
    HOOKPY_ENABLE = False


def set_config_path(path: str):
    global HOOKPY_CONFIG_PATH
    HOOKPY_CONFIG_PATH = path


def find_enable_hook(func_id):
    if not HOOKPY_ENABLE:
        return None
    if func_id not in _FUNC_ID_TO_HOOKS:
        return None
    hooks = _FUNC_ID_TO_HOOKS[func_id]
    impl = None
    if len(hooks) == 1:
        hook = hooks[0]
        if hook.enabled():
            hook.is_enabled(True)
            impl = hook.get_impl()
        else:
            hook.is_enabled(False)
        return impl
    found = False
    for i in range(len(hooks)):
        hook = hooks[i]
        if hook.enabled() and not found:
            impl = hook.get_impl()
            found = True
            hook.is_enabled(True)
        else:
            hook.is_enabled(False)
    return impl


def register_hook(func=None):
    def wrapper(func):
        if not HOOKPY_ENABLE:
            return func
        if compat.Python3_6AndLater:
            if inspect.isasyncgenfunction(func):
                return func

        # we need to know the function type, regular/generator/async/async generator
        # with/async with isn't supported.
        func_without_deco = try_remove_decorator(func)
        path = inspect.getsourcefile(func_without_deco)
        if path is None:
            return func
        func_id = funcid.get_func_id_by_object(func_without_deco)
        func_name = ""
        if func_id is None:
            # get full path
            local_parts = funcid.get_func_id_by_object(func_without_deco,
                                                       local=True)
            func_id = str(path) + "-" + local_parts
            func_name = local_parts[-1]
        else:
            _, _, local_parts = funcid.split_func_id(func_id)
            func_name = local_parts[-1]
        for pattern in HOOK_CONFIG.func_excludes:
            if pattern.match(func_name):
                return func
        with _LOCK:
            if func_id in _FUNC_ID_TO_HOOKS:
                return func
            hooks = []
            for hook_cls, config in HOOK_CONFIG.get_hook_classes():
                hook = hook_cls(**config)
                if hook.create_impl(func_id, func):
                    hooks.append(hook)
            if hooks:
                _FUNC_ID_TO_HOOKS[func_id] = hooks
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapped(*args, **kw):
                impl = find_enable_hook(func_id)
                if not impl:
                    impl = func
                return await impl(*args, **kw)

            return async_wrapped
        if inspect.isgeneratorfunction(func):

            @functools.wraps(func)
            def generator_wrapped(*args, **kw):
                impl = find_enable_hook(func_id)
                if not impl:
                    impl = func
                yield from impl(*args, **kw)

            return generator_wrapped
        else:

            @functools.wraps(func)
            def regular_wrapped(*args, **kw):
                impl = find_enable_hook(func_id)
                if not impl:
                    impl = func
                return impl(*args, **kw)

            return regular_wrapped

    if func is None:
        return wrapper
    else:
        return wrapper(func)


class Hook(abc.ABC):
    @abc.abstractmethod
    def create_impl(self, func_id: str, func) -> bool:
        """hook init impl. if failed, return a False,
        this hook won't be added to collection.
        """

    @abc.abstractmethod
    def get_impl(self):
        """get a impl.
        """

    @abc.abstractmethod
    def enabled(self) -> bool:
        """this hook may not be used even if it return True. 
        keep in mind that to minimize running overhead, the hook impl
        shouldn't be used for all time.
        """

    @abc.abstractmethod
    def is_enabled(self, enabled: bool):
        """reset your state here.
        """

    def handle_exit(self):
        return


def _hook_exit():
    for _, hooks in _FUNC_ID_TO_HOOKS.items():
        for h in hooks:
            h.handle_exit()


atexit.register(_hook_exit)
