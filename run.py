from os import system
from gpg_constants import GPG_CONF_PATH, GPG_AGENT_CONF_PATH

# setup gpg config

system(f"cp gpg.conf {GPG_CONF_PATH}")
system(f"cp gpg-agent.conf {GPG_AGENT_CONF_PATH}")

# generat data and keys, sign, and verify

system("python gpg_constants.py")
system("python gen_random_data.py")
system("python gpg_gen_keys.py")
system("python gpg_sign_files.py")
system("python gpg_verify_sig.py")
system("python rainbow.py")
