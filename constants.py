import pathlib

ROOT = pathlib.Path(__file__).parent

# TODO key sizes

KEYS = {
    'EDDSA' : [256],
    'DSA'   : [768, 896, 1024],
    'RSA'   : [1024, 2048, 3072, 4096],
#    'ELG'   : [1024, 2048, 3072, 4096],
#    'ECDH'  : [1024, 2048, 3072, 4096],
#    'ECDSA' : [1024, 2048, 3072, 4096],
}

# test parameters

NUM_DATA : int = 10
'''
Number of randomly generated data files
'''

NUM_KEYS : int = 2
'''
Number of keys per type and length
'''

# dir constants

DATA_DIR = ROOT / "data"
'''
Data directory path
'''

KEYS_DIR = ROOT / 'keys'
'''
Keys directory path
'''

SIGS_DIR = ROOT / "sigs"
'''
Sigs directory path
'''
