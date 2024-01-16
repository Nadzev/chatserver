from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad  # Import padding functions

import camellia


class RSAHandler:
    "RSA class to encrypt and decrypt messages"

    @staticmethod
    def generate_rsa_keys():
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    @classmethod
    def rsa_encrypt(cls, public_key, data):
        recipient_key = RSA.import_key(public_key)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        return cipher_rsa.encrypt(data)

    @classmethod
    def rsa_decrypt(cls, private_key, encrypted_data):
        private_key = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        return cipher_rsa.decrypt(encrypted_data)


class CamelliaMessageHandler:
    "Camellia class to encrypt and decrypt messages"

    @classmethod
    def camellia_encrypt(cls, key, data):
        message = bytes(data, "utf-8")
        byte_key = bytes.fromhex(key)

        c1 = camellia.CamelliaCipher(
            key=byte_key, IV=b"16 byte iv. abcd", mode=camellia.MODE_CBC
        )
        padded_data = pad(message, 16)
        ciphertext = c1.encrypt(padded_data)
        return ciphertext

    @classmethod
    def camellia_decrypt(cls, key, ciphertext, iv):
        byte_text = bytes.fromhex(ciphertext)
        byte_key = bytes.fromhex(key)
        c1 = camellia.CamelliaCipher(
            key=byte_key, IV=b"16 byte iv. abcd", mode=camellia.MODE_CBC
        )
        decrypted_text = c1.decrypt(byte_text)
        decrypted_text = unpad(decrypted_text, 16)
        return decrypted_text
