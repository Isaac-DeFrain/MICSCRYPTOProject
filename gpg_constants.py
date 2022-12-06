'''
GPG constants
'''

import os
import json
import key_ops
import file_ops
import pathlib as pl
import constants as cs

# gpg config paths

GPG_CONF_PATH = pl.Path("~/.gnupg/gpg.conf")
GPG_AGENT_CONF_PATH = pl.Path("~/.gnupg/gpg-agent.conf")

protected_gpg_keys_path = cs.KEYS_DIR / "protected_gpg_keys.json"

def key_names_and_ids():
    og_gpg_keys_path = cs.KEYS_DIR / "og_gpg_keys"
    protected_gpg_keys_dict = {}
    # only protect original gpg keys
    if not og_gpg_keys_path.exists():
        os.system(f'gpg -k > {og_gpg_keys_path}')
        with og_gpg_keys_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            # get key names
            key_files = filter(lambda s: s.startswith("uid"), lines)
            key_names = [key_ops.get_full_key_name(key_file) for key_file in key_files]
            # get key ids
            lines_ids = filter(lambda s: s.startswith(" "), lines)
            key_ids = [line.strip() for line in lines_ids]
        protected_gpg_keys_dict["names"] = key_names
        protected_gpg_keys_dict["ids"] = key_ids
        with protected_gpg_keys_path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(protected_gpg_keys_dict, indent=4))
            f.close()

# create gpg keys and sigs dirs

file_ops.mkdir(cs.KEYS_DIR)
file_ops.mkdir(cs.SIGS_DIR)
key_names_and_ids()

# original gpg key ids

def protected_gpg_ids() -> "set[str]":
    with protected_gpg_keys_path.open("r", encoding="utf-8") as f:
        dict = json.load(f)
        return dict["ids"]

# original gpg key names

def protected_gpg_names() -> "set[str]":
    with protected_gpg_keys_path.open("r", encoding="utf-8") as f:
        dict = json.load(f)
        return dict["names"]

# protected gpg keys

PROTECTED_GPG_NAMES = protected_gpg_names()
'''
GPG key names we don't want to delete
'''

PROTECTED_GPG_IDS = protected_gpg_ids()
'''
GPG key ids we don't want to delete
'''
