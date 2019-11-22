import hashlib


def hash_build_name(name, tag):
    return hashlib\
        .sha256(f'{name}{tag}'.encode())\
        .hexdigest()
