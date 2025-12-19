import hashlib

def sha256_checksum(filename):
    """Calculate the SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()