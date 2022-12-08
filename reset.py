from os import system
from constants import *
from pathlib import Path
from shutil import rmtree
from gpg_constants import *
from rainbow import RAINBOW_ROOT
from gpg_sign_files import get_key_ids_and_paths

def delete_gpg_keys():
    '''
    Deletes all unprotected GPG secret and public keys
    '''
    for key_id, _ in get_key_ids_and_paths():
        system(f'gpg --batch --yes --delete-secret-and-public-keys {key_id}')

def delete_dir(dpath: Path):
    if dpath.exists():
        rmtree(dpath)

if __name__ == "__main__":
    delete_gpg_keys()
    # delete data, keys, sigs dirs
    delete_dir(DATA_DIR)
    delete_dir(KEYS_DIR)
    delete_dir(SIGS_DIR)
    delete_dir(RAINBOW_ROOT)
    # reset gpg config
    system(f'echo "" > {GPG_CONF_PATH}')
    system(f'echo "" > {GPG_AGENT_CONF_PATH}')
