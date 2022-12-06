'''
Benchmark rainbow: key gen, sign, and verify
'''

from os import system, chdir, listdir
from file_ops import *
from benchmark import *
from constants import *
from pathlib import Path

RAINBOW_ROOT = ROOT / "rainbow"
RAINBOW_KEYS = RAINBOW_ROOT / "keys"
RAINBOW_SIGS = RAINBOW_ROOT / "sigs"
RAINBOW_SRC_DIR = ROOT / "rainbow-submission-round2"
RAINBOW_SRC_GITIGNORE = RAINBOW_ROOT / "sigs"

def rainbow_exe(exe: Path, path: Path):
    system(f"{exe} > {path}")

# create rainbow dirs

mkdir(RAINBOW_ROOT)
mkdir(RAINBOW_KEYS)
mkdir(RAINBOW_SIGS)

def add_gitignore():
    fpath = ROOT / "template_gitignore"
    with fpath.open("r", encoding="utf-8") as f:
        contents = f.read()
        f.close()
    write_file(RAINBOW_SRC_GITIGNORE, contents)

# clone the rainbow repo and add .gitignore in project root

if not RAINBOW_SRC_DIR.exists():
    system("git clone https://github.com/fast-crypto-lab/rainbow-submission-round2.git")
    add_gitignore()

##### reference implementation #####

# ref root dir

RAINBOW_REF_DIR  = RAINBOW_SRC_DIR / "Reference_Implementation"

# ref keys and signatures dirs

RAINBOW_REF_KEYS = RAINBOW_KEYS / "reference"
RAINBOW_REF_SIGS = RAINBOW_SIGS / "reference"

# ref binary paths

RAINBOW_REF_GEN = RAINBOW_REF_DIR / "rainbow-genkey"
RAINBOW_REF_SGN = RAINBOW_REF_DIR / "rainbow-sign"
RAINBOW_REF_VRF = RAINBOW_REF_DIR / "rainbow-verify"

# ref stats paths

RAINBOW_REF_GEN_STATS = RAINBOW_REF_KEYS / "rainbow_ref_gen_stats.json"
RAINBOW_REF_SGN_STATS = RAINBOW_REF_SIGS / "rainbow_ref_sign_stats.json"
RAINBOW_REF_VRF_STATS = RAINBOW_REF_SIGS / "rainbow_ref_verify_stats.json"

# ref create dirs

mkdir(RAINBOW_REF_DIR)
mkdir(RAINBOW_REF_KEYS)
mkdir(RAINBOW_REF_SIGS)

# ref make binaries if they don't exist already

if not (RAINBOW_REF_GEN.exists()
        and RAINBOW_REF_SGN.exists()
        and RAINBOW_REF_VRF.exists()):
    chdir(RAINBOW_REF_DIR)
    system("make")
    chdir(ROOT)

# ref benchmark

ref_gen_times = {}
ref_sign_times = {}
ref_verify_times = {}

# ref generate key, sign data, and verify

for n in range(NUM_KEYS):
    key_path = RAINBOW_REF_KEYS / f"rainbow_{n}"
    benchmark(rainbow_exe(RAINBOW_REF_GEN, key_path), ref_gen_times, n)
    for datum in listdir(DATA_DIR):
        sig_path = RAINBOW_REF_SIGS / f"{n}-{datum}.sig"
        benchmark(rainbow_exe(RAINBOW_REF_SGN, sig_path), ref_sign_times, n)
    for sigs in filter(lambda s: s.startswith(str(n)), listdir(RAINBOW_REF_SIGS)):
        verify_path = RAINBOW_REF_SIGS / f"{n}.verify"
        benchmark(rainbow_exe(RAINBOW_REF_VRF, verify_path), ref_verify_times, n)

# ref dump stats

write_file(RAINBOW_REF_GEN_STATS, dumps(ref_gen_times, indent = 4))
write_file(RAINBOW_REF_SGN_STATS, dumps(ref_sign_times, indent = 4))
write_file(RAINBOW_REF_VRF_STATS, dumps(ref_verify_times, indent = 4))

##### optimized implementation #####

# amd64 optimized root dir

RAINBOW_OPT_DIR  = RAINBOW_SRC_DIR / "Optimized_Implementation/amd64"

# opt keys and signatures dirs

RAINBOW_OPT_KEYS = RAINBOW_KEYS / "optimized"
RAINBOW_OPT_SIGS = RAINBOW_SIGS / "optimized"

# opt binary paths

RAINBOW_OPT_GEN  = RAINBOW_OPT_DIR / "rainbow-genkey"
RAINBOW_OPT_SGN  = RAINBOW_OPT_DIR / "rainbow-sign"
RAINBOW_OPT_VRF  = RAINBOW_OPT_DIR / "rainbow-verify"

# opt stats paths

RAINBOW_OPT_GEN_STATS = RAINBOW_OPT_KEYS / "rainbow_opt_gen_stats.json"
RAINBOW_OPT_SGN_STATS = RAINBOW_OPT_SIGS / "rainbow_opt_sign_stats.json"
RAINBOW_OPT_VRF_STATS = RAINBOW_OPT_SIGS / "rainbow_opt_verify_stats.json"

# opt create dirs

mkdir(RAINBOW_OPT_DIR)
mkdir(RAINBOW_OPT_KEYS)
mkdir(RAINBOW_OPT_SIGS)

# opt make binaries if they don't exist already

if not (RAINBOW_OPT_GEN.exists()
        and RAINBOW_OPT_SGN.exists()
        and RAINBOW_OPT_VRF.exists()):
    chdir(RAINBOW_OPT_DIR)
    system("make")
    chdir(ROOT)

# opt benchmark

opt_gen_times = {}
opt_sign_times = {}
opt_verify_times = {}

# opt generate key, sign data, and verify

for n in range(NUM_KEYS):
    key_path = RAINBOW_OPT_KEYS / f"rainbow_{n}"
    benchmark(rainbow_exe(RAINBOW_OPT_GEN, key_path), opt_gen_times, n)
    for datum in listdir(DATA_DIR):
        sig_path = RAINBOW_OPT_SIGS / f"{n}-{datum}.sig"
        benchmark(rainbow_exe(RAINBOW_OPT_SGN, sig_path), opt_sign_times, n)
    for sigs in filter(lambda s: s.startswith(str(n)), listdir(RAINBOW_OPT_SIGS)):
        verify_path = RAINBOW_OPT_SIGS / f"{n}.verify"
        benchmark(rainbow_exe(RAINBOW_OPT_VRF, verify_path), opt_verify_times, n)

# opt dump stats

write_file(RAINBOW_OPT_GEN_STATS, dumps(opt_gen_times, indent = 4))
write_file(RAINBOW_OPT_SGN_STATS, dumps(opt_sign_times, indent = 4))
write_file(RAINBOW_OPT_VRF_STATS, dumps(opt_verify_times, indent = 4))
