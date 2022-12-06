def key_file_template(key_type: str, key_len: int, num: int, pwd: str):
    '''
    GPG key file template
    '''
    return f'''\
Key-Type: {key_type}
Key-Length: {key_len}
Name-Real: {key_type}
Name-Comment: {num}
Name-Email: {key_type}_{key_len}_{num}
Expire-Date: 0
Passphrase: {pwd}
%commit
'''