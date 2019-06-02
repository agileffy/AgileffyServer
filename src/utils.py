import binascii,hashlib
def encrypt(password,salt):
    print('DEBUG:')
    print(password)
    print(salt)
    return binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 10000))
