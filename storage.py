import argparse
import os
import tempfile
import json
from json.decoder import JSONDecodeError


storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
parser = argparse.ArgumentParser()
parser.add_argument("--key")
parser.add_argument("--value")
args = parser.parse_args()

value = args.value
key = args.key

try:
    fr = open(storage_path, 'r')
    key_value_storage = json.load(fr)
except OSError:
    key_value_storage = {}
except JSONDecodeError:
    key_value_storage = {}

if value is not None and key is not None:
    if key not in key_value_storage:
        key_value_storage[key] = [value]
    else:
        key_value_storage[key].append(value)
    with open(storage_path, 'w') as fw:
        json.dump(key_value_storage, fw)
elif key is not None:
    if key in key_value_storage.keys():
        print(', '.join(key_value_storage[key]))
    else:
        print(' ')
