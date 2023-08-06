import os
import runpy
import subprocess
import sys
from pathlib import Path

import hookpy.core
from hookpy import hookimport
from hookpy.constants import HOOKPY_CONFIG_PATH_NAME, HOOKPY_ENABLE_NAME
from hookpy.core import HOOK_CONFIG


def main():
    env = os.environ.copy()
    env[HOOKPY_ENABLE_NAME] = "1"
    config_path = Path(sys.argv[1])
    assert config_path.exists()
    env[HOOKPY_CONFIG_PATH_NAME] = sys.argv[1]
    subprocess.run(["python", *sys.argv[2:]],
                   stdout=sys.stdout,
                   stderr=sys.stderr,
                   env=env)


def auto_main_forward():
    """we need forward in subprocess
    because there is a argument 'config path' that will break
    arg parse of python.
    """
    env = os.environ.copy()
    env[HOOKPY_ENABLE_NAME] = "1"
    config_path = Path(sys.argv[1])
    assert config_path.exists()
    env[HOOKPY_CONFIG_PATH_NAME] = sys.argv[1]
    subprocess.run(["__hookpy-auto-main", *sys.argv[2:]],
                   stdout=sys.stdout,
                   stderr=sys.stderr,
                   env=env)


def auto_main():
    hookimport.install_register_hook(HOOK_CONFIG.hook_folders)
    sys.path.append(str(Path(sys.argv[1]).parent))
    runpy.run_path(sys.argv[1], run_name="__main__")


def auto_main_auto_find_config():
    """we assume a config file 'hook-config.json' is inside current dir.
    """
    found = False
    candidate = None
    for parent in Path.cwd().parents:
        candidate = parent / 'hook-config.json'
        if candidate.exists():
            found = True
            break
    if not found:
        raise ValueError(
            "you need to provide a hook-config.json in cwd or cwd.parents")
    hookpy.core.set_config_path(str(candidate))
    hookpy.core.enable_hook()
    hookpy.core.init_hook_config()
    hookimport.install_register_hook(HOOK_CONFIG.hook_folders)
    sys.path.append(str(Path(sys.argv[1]).parent))
    runpy.run_path(sys.argv[1], run_name="__main__")
