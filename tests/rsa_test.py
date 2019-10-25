import unittest
from client.signature_encrypter import SignatureEncrypter
from server.signature_decrypter import SignatureDecrypter


class RSATest(unittest.TestCase):
    def test_signature(self):
        signature = SignatureEncrypter.encrypt_signature("id_rsa_test")
        self.assertEqual(SignatureDecrypter.decrypt_signature("id_rsa_test.pub", signature),
                         SignatureDecrypter.valid_signature)


if __name__ == '__main__':
    unittest.main()
