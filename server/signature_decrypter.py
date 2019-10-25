from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from common.signature import signature_message


class SignatureDecrypter:

    @staticmethod
    def decrypt(signature: bytes) -> str:
        key = RSA.import_key(open('public_key.der').read())
        h = SHA256.new(signature_message)
        verifier = pss.new(key)
        try:
            verifier.verify(h, signature)
            return "The signature is valid."
        except (ValueError, TypeError):
            return "The signature is not valid."
