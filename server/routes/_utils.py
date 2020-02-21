import hashlib

def get_file(name):
    with open(f"server/static/{name}.tar.gz", "rb") as f:
        return f.read()

def get_hash(content):
    base = hashlib.sha256()
    base.update(content)
    return base.hexdigest()

def get_file_and_hash(name):
    data = get_file(name)
    return get_hash(data), data
