from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from common.signature_message import signature_message


class SignatureDecrypter:
    valid_signature: str = "The signature is valid."
    invalid_signature: str = "The signature is not valid."

    @staticmethod
    def decrypt_signature(key_file: str, signature: bytes) -> str:
        key = RSA.import_key(open(key_file).read())
        h = SHA256.new(signature_message)
        verifier = pss.new(key)
        try:
            verifier.verify(h, signature)
            return SignatureDecrypter.valid_signature
        except (ValueError, TypeError):
            return SignatureDecrypter.invalid_signature
