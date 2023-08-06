import hashlib

BUF_SIZE = 65536


def hash_file(filename):
    """
    Calculate a SHA-512 hash from the given file.
    :param filename: File from which the hash should be calculated
    :return:
    """
    sha512 = hashlib.sha512()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha512.update(data)

    return sha512.hexdigest()

