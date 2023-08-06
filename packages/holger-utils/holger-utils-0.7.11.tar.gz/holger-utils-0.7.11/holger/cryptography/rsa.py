from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from binascii import hexlify


class RSAEncryption:

    def __init__(self, private_key=None):
        if private_key is None:
            setattr(self, '__private_key__', RSA.generate(2048))
        else:
            setattr(self, '__private_key__', private_key)

    @property
    def private_key(self):
        """
        :return: return private key with 2048 bits
        """
        return getattr(self, '__private_key__').export_key().decode()

    def public_key(self):
        return getattr(self, '__private_key__').public_key().export_key().decode()

    def import_key(self, path):
        return RSA.import_key(open(path, 'r').read())

    def encrypt(self, message):
        private_key = getattr(self, '__private_key__')
        cipher = PKCS1_OAEP.new(
            key=private_key,
            hashAlgo=SHA256
        )
        encrypted_message = cipher.encrypt(message=message)
        return encrypted_message

    def decrypt(self, public_key, encrypted_message):
        decrypt = PKCS1_OAEP.new(key=public_key)
        decrypted_message = decrypt.decrypt(encrypted_message)
        return decrypted_message
