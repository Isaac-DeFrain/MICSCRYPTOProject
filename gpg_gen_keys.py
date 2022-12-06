'''
Benchmark GPG key generation
'''

from benchmark import *
from key_ops import *
from constants import *
from pathlib import Path
from secrets import token_hex
from os import system, listdir
from file_ops import write_file
from key_file_template import *
from gpg_constants import KEYS_DIR

# key generation utils

def is_key_dir(fname: str) -> bool:
    fpath = KEYS_DIR / fname
    return fname in KEYS.keys() and fpath.is_dir()

def key_gen_file(key_type: str, key_len: int, num: int):
    '''
    Generate a gpg key file for unattended batch key generation
    '''
    fpath = KEYS_DIR / key_type / f'{key_type}_{key_len}_{num}'
    pwd = token_hex(32)
    contents = key_file_template(key_type, key_len, num, pwd)
    write_file(fpath, contents)

def stats_file(key_type: str):
    return KEYS_DIR / f"{key_type}_gen_stats.json"

def key_gen(fpath: Path):
    '''
    Generate gpg key from file `fpath`
    '''
    system(f'gpg --batch --generate-key {fpath}')

if __name__ == "__main__":
    # generate key files
    for key_type in KEYS.keys():
        for num in range(NUM_KEYS):
            for key_len in KEYS[key_type]:
                key_gen_file(key_type, key_len, num)

    # generate keys from files
    for key_type in filter(is_key_dir, listdir(KEYS_DIR)):
        key_type_times = {}
        key_type_dir = KEYS_DIR / key_type
        groups = key_groups(listdir(key_type_dir), key_type)
        for n, key_files in groups:
            for key_file in key_files:
                key_path = key_type_dir / key_file
                benchmark(key_gen(key_path), key_type_times, n)
        write_file(stats_file(key_type), dumps(key_type_times, indent=4))
