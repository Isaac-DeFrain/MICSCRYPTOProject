'''
Benchmark GPG signatures
'''

from key_ops import *
from file_ops import *
from benchmark import *
from constants import *
from pathlib import Path
from gpg_constants import *
from os import system, listdir

def get_pwd(key_file_lines: "list[str]"):
    res = ""
    for line in key_file_lines:
        if line.startswith("Passphrase"):
            res = line.split(":")[1].strip()
    return res

def is_unprotected_key(key_name: str) -> bool:
    return all([not key_name.startswith(pname) for pname in PROTECTED_GPG_NAMES])

def get_full_key_name(key_file: str) -> str:
    return key_file.split("<")[1].split(">")[0]

def mk_key_path(key_name: str) -> Path:
    return KEYS_DIR / get_key_type(key_name) / key_name

def stats_file(sig_type: str) -> Path:
    return SIGS_DIR / f"{sig_type}_sign_stats.json"

def get_key_ids_and_paths() -> "list[tuple[str, Path]]":
    all_keys_path = KEYS_DIR / "all_keys"
    # print gpg keys to all_keys_path
    mkdir(KEYS_DIR)
    system(f'gpg -k > {all_keys_path}')
    with all_keys_path.open("r", encoding="utf8") as f:
        lines = f.readlines()
        # get key ids
        lines_ids = filter(lambda s: s.startswith(" "), lines)
        lines_ids = [line.strip() for line in lines_ids]
        key_ids = filter(lambda s: s not in PROTECTED_GPG_IDS, lines_ids)
        # get key file paths
        key_files = filter(lambda s: s.startswith("uid"), lines)
        key_files = [get_full_key_name(key_file) for key_file in key_files]
        key_files = filter(is_unprotected_key, key_files)
        key_paths = [mk_key_path(key_file) for key_file in key_files]
    return list(zip(key_ids, key_paths))

def sign(fname: str, key_id: str, sig_path: Path, pwd: str):
    '''
    GPG sign the file with the given key and passphrase
    '''
    system(f"echo {pwd} | gpg --batch --yes -u {key_id} -o {sig_path} --passphrase-fd 0 --sign {DATA_DIR / fname}")

if __name__ == "__main__":
    times = {}
    for key_id, key_path in get_key_ids_and_paths():
        key_name = key_path.name
        n = get_key_len(key_name)
        sig_type = get_key_type(key_name)
        sig_type_dir = SIGS_DIR / sig_type
        for datum in sorted(listdir(DATA_DIR)):
            sig_path = sig_type_dir / f"{key_name}-{datum}.sig"
            mkdir(sig_type_dir)
            with key_path.open("r", encoding="utf-8") as f:
                pwd = get_pwd(f.readlines())
            try:
                times[sig_type]
            except KeyError:
                times[sig_type] = {}
            benchmark(sign(datum, key_id, sig_path, pwd), times[sig_type], n)
    for key_type in KEYS.keys():
        write_file(stats_file(key_type), dumps(times[key_type], indent=4))
