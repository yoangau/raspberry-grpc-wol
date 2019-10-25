from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pss

from common.signature_message import signature_message


class SignatureEncrypter:

    @staticmethod
    def encrypt_signature(key_file: str) -> bytes:
        key = RSA.import_key(open(key_file).read())
        h = SHA256.new(signature_message)
        signature = pss.new(key).sign(h)
        return signature
