import contextlib
import os
import shutil
import sys
import tempfile
import uuid
from pathlib import Path


@contextlib.contextmanager
def fake_project(project_path):
    dirpath = tempfile.mkdtemp()
    proj_path = None
    try:
        proj_name = "__hookpy_fake_project" + uuid.uuid4().hex[:8]
        project_path_copied = Path(dirpath).resolve() / proj_name
        shutil.copytree(str(project_path), str(project_path_copied))
        proj_path = str(project_path_copied.parent)
        sys.path.append(proj_path)
        yield proj_name, Path(proj_path)
    finally:
        shutil.rmtree(dirpath)
        if proj_path is not None:
            sys.path.pop()
