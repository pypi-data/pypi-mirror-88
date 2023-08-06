import ast
import importlib
import inspect
import re
import runpy
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Deque, Dict, List, Optional, Tuple, Union

from hookpy import loader


def parse_source_path(
        source_path: Union[Path, str]) -> Tuple[ast.AST, List[str]]:
    source_path = str(source_path)
    if source_path[0] == "<" and source_path[-1] == ">":
        # https://github.com/cool-RR/PySnooper/blob/master/pysnooper/tracer.py
        ipython_filename_pattern = re.compile('^<ipython-input-([0-9]+)-.*>$')
        ipython_filename_match = ipython_filename_pattern.match(source_path)
        if ipython_filename_match:
            entry_number = int(ipython_filename_match.group(1))
            import IPython
            ipython_shell = IPython.get_ipython()
            ((_, _, source_chunk),) = ipython_shell.history_manager. \
                                get_range(0, entry_number, entry_number + 1)
            source = source_chunk
        else:
            raise NotImplementedError
    else:
        with open(source_path, "r") as f:
            source = f.read()
    return ast.parse(source), source.split("\n")


def try_remove_decorator(func):
    if isinstance(func, staticmethod):
        # TODO: drop staticmethod support?
        return func
    if hasattr(func, "__wrapped__"):
        return try_remove_decorator(func.__wrapped__)
    else:
        try:
            inspect.getfile(func)
            return func
        except TypeError as e:
            err_msg = "your decorator must use __wrapped__ to save wrapped object like functools.wraps"
            print(err_msg)
            raise e


def get_toplevel_func_node(tree: ast.AST):
    from collections import deque
    res = []  # type: List[Tuple[ast.AST, List[ast.AST]]]
    todo = deque([(tree.body, [])
                  ])  # type: Deque[Tuple[List[ast.AST], List[ast.AST]]]
    while todo:
        body, cur_parent_ns = todo.popleft()
        for node in body:
            if isinstance(node, (ast.ClassDef)):
                todo.append((node.body, [*cur_parent_ns, node]))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                res.append((node, cur_parent_ns))
    return res


def find_toplevel_func_node_by_lineno(tree: ast.AST, lineno: int):
    from collections import deque
    todo = deque([(tree.body, [])
                  ])  # type: Deque[Tuple[List[ast.AST], List[ast.AST]]]
    while todo:
        body, cur_parent_ns = todo.popleft()
        for node in body:
            if isinstance(node, (ast.ClassDef)):
                todo.append((node.body, [*cur_parent_ns, node]))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.lineno == lineno:
                    return (node, cur_parent_ns)
                elif node.lineno > lineno:
                    break
    return None


def split_func_id(
        fid: str,
        path_delimiter: str = ".",
        local_delimiter: str = "-") -> Tuple[List[str], str, List[str]]:
    relative_path_parts = list(fid.split(path_delimiter))
    filename_local_id = relative_path_parts[-1]
    local_parts = filename_local_id.split(local_delimiter)
    filename = local_parts[0]
    return relative_path_parts[:-1], filename, local_parts[1:]


def get_func_id_by_object(func,
                          root: Optional[Union[Path, str]] = None,
                          local: bool = False):
    func = try_remove_decorator(func)
    _, lineno = inspect.getsourcelines(func)
    path = inspect.getsourcefile(func)
    tree, _ = parse_source_path(path)

    func_node_meta = find_toplevel_func_node_by_lineno(tree, lineno)
    if func_node_meta is None:
        return None
    func_node, parents = func_node_meta
    names = [n.name for n in parents + [func_node]]
    if local:
        return "-".join(names)

    if root is not None:
        relative_path = Path(path).relative_to(Path(root))
        import_parts = list(relative_path.parts)
        import_parts[-1] = relative_path.stem
    else:
        if not loader.is_path_in_package(path):
            return None
        import_parts = loader.try_capture_import_parts(path, None)
    func_id = ".".join(import_parts) + "-" + "-".join(names)
    return func_id


def modify_func_of_file(tree: ast.AST, mod: ModuleType,
                        modifier: Callable[[Dict[str, Any], str, Any], None]):
    module_dict = mod.__dict__

    for node, parent_classes in get_toplevel_func_node(tree):
        mod_key_names = [n.name for n in parent_classes]
        names = mod_key_names + [node.name]
        if len(names) == 1:
            if names[0] not in module_dict:
                continue
            mod_set_attr = lambda k, v: setattr(mod, k, v)
            modifier(mod, names[0], mod_set_attr)
        else:
            if names[0] not in module_dict:
                continue
            obj = module_dict[names[0]]
            invalid = False
            for part in names[1:-1]:
                if part in dir(obj):
                    obj = getattr(obj, part)
                else:
                    invalid = True
                    break
            if invalid:
                continue
            if names[-1] not in dir(obj):
                continue
            mod_set_attr = lambda k, v: setattr(obj, k, v)
            modifier(obj, names[-1], mod_set_attr)


def get_module_object_by_imp_id(imp_id, use_path=False):
    # imp_id: mod.submod.submod2::ObjectName
    parts = imp_id.split("::")
    module_import_path = parts[0]
    local_parts = parts[1:]
    if not use_path:
        mod = importlib.import_module(module_import_path)
        module_dict = mod.__dict__
    else:
        module_dict = runpy.run_path(str(module_import_path))
    # mod = importlib.reload(mod)
    obj = module_dict[local_parts[0]]
    for part in local_parts[1:]:
        obj = getattr(obj, part)
    return obj
