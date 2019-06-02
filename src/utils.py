import binascii,hashlib
def encrypt(password,salt):
    return binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 10000))
