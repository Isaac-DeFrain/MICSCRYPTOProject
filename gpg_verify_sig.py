'''
Benchmark GPG verify signatures
'''

from key_ops import *
from benchmark import *
from constants import *
from pathlib import Path
from os import listdir, system
from file_ops import write_file
from gpg_sign_files import get_key_ids_and_paths

def get_key_len(fname: str) -> int:
    return int(fname.split("_")[1])

def is_sig_dir(fname: str) -> bool:
    fpath = SIGS_DIR / fname
    return fname in KEYS.keys() and fpath.is_dir()

def is_sig_file(fname: str) -> bool:
    suffix = fname.split(".")[-1]
    return suffix == "sig"

def stats_file(sig_type: str) -> Path:
    return SIGS_DIR / f"{sig_type}_verify_stats.json"

verify_path = SIGS_DIR / "verify"

def verify(fname: str, key_id: str, sig_type: str):
    '''
    GPG verify signature and append output to `verify_path`
    '''
    system(f"gpg --batch --yes -u {key_id} --verify {SIGS_DIR / sig_type / fname} >> {verify_path}")

if __name__ == "__main__":
    write_file(verify_path)
    for sig_type in filter(is_sig_dir, listdir(SIGS_DIR)):
        key_type_times = {}
        sig_type_dir = SIGS_DIR / sig_type
        for sig_name in filter(is_sig_file, listdir(sig_type_dir)):
            # sig_name = {key_name}-{datum}.sig
            key_name = sig_name.split("-")[0]
            n = get_key_len(key_name)
            for key_id, key_path in get_key_ids_and_paths():
                if key_name == key_path.name:
                    benchmark(verify(sig_name, key_id, sig_type), key_type_times, n)
        write_file(stats_file(sig_type), dumps(key_type_times, indent=4))
