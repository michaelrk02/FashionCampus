import hashlib
import random
import string

def password_make(password):
    salt = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k = 16))
    hash = password_hash(password, salt)
    return (hash, salt)

def password_check(password, hash, salt):
    return password_hash(password, salt) == hash

def password_hash(password, salt):
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
