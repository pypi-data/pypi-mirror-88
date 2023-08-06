import os
from copy import deepcopy


def deep_find_files(path, extensions):
    paths = []
    if not os.path.isdir(path):
        raise ValueError("{} is not a valid directory".format(path))
    for root, dirs, files in os.walk(path):
        for fname in files:
            if fname.split(".")[-1] in extensions:
                paths.append(os.path.join(root, fname))
    return paths

def find_yaml_files(path):
    return deep_find_files(path, ["yaml", "yml"])

def find_json_files(path):
    return deep_find_files(path, ["json"])

def read_endpoint_files(root):
    import yaml
    import json
    import os
    domain = {}
    for path in find_yaml_files(root): 
        with open(path, "r") as f:
            domain.update(yaml.safe_load(f))

    for path in find_json_files(root): 
        with open(path, "r") as f:
            domain.update(json.safe_load(f))
    return domain

def read_endpoint_dirs(roots):
    domain = {}
    for root in roots:
        domain.update(read_endpoint_files(root))
