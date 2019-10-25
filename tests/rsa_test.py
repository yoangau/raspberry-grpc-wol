import unittest
from client.signature_encrypter import SignatureEncrypter
from server.signature_decrypter import SignatureDecrypter


class RSATest(unittest.TestCase):
    def test_signature_should_work(self):
        signature = SignatureEncrypter.encrypt_signature("id_rsa_test")
        self.assertEqual(SignatureDecrypter.decrypt_signature("id_rsa_test.pub", signature),
                         SignatureDecrypter.valid_signature)

    def test_signature_should_not_work(self):
        self.assertEqual(SignatureDecrypter.decrypt_signature("id_rsa_test.pub", bytes("not_valid", encoding='utf-8')),
                         SignatureDecrypter.invalid_signature)


if __name__ == '__main__':
    unittest.main()
