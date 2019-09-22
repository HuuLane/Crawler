__all__ = ["write_file", "log", "files", "remove_dir", "Dict", "save_jsonify"]


# typing hint
from typing import List, Iterable

# os
import os
from os import listdir
from os.path import isfile, join


def save_jsonify(data, path):
    import json
    str = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+') as f:
        f.write(str)


def remove_dir(path: str):
    from shutil import rmtree
    rmtree(path)


def files(dir_path: str) -> Iterable[str]:
    '''
    return files list by dir path
    '''
    r = []
    try:
        for f in listdir(dir_path):
            f_path = join(dir_path, f)
            if isfile(f_path):
                r.append(f_path)
        r.sort()
    except FileNotFoundError:
        pass
    finally:
        return r


def check_dir(filename: str):
    '''
    return dir path
    '''
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        log('Create dir:', d)
        os.makedirs(d)


def write_file(filename: str, context: str) -> None:
    '''
    write file by filename(with path)
    '''
    check_dir(filename)
    with open(filename, 'w+', encoding='UTF-8') as f:
        f.write(context)


def log(*args, **kwargs) -> None:
    print(*args, **kwargs)


class Dict(dict):
    '''
    dot.notation access to dictionary attributes
    '''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
