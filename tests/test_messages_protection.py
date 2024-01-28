from Crypto.Random import get_random_bytes

from chat.use_cases.messages_protection import (CamelliaMessageHandler,
                                                RSAHandler)

# Example Usage
alice_private, alice_public = RSAHandler.generate_rsa_keys()
bob_private, bob_public = RSAHandler.generate_rsa_keys()

# Alice sends a message to Bob
symmetric_key = get_random_bytes(32)  # 256-bit key for Camellia
encrypted_key = RSAHandler.rsa_encrypt(bob_public, symmetric_key)
print(encrypted_key)

# Encrypt the message with Camellia
message = bytes("olá como vai?", "utf-8")
camellia_encrypted_msg = CamelliaMessageHandler.camellia_encrypt(symmetric_key, message)
print("Encrypted message: ", camellia_encrypted_msg)

# Bob receives the message
decrypted_key = RSAHandler.rsa_decrypt(bob_private, encrypted_key)
decrypted_msg = CamelliaMessageHandler.camellia_decrypt(
    decrypted_key, camellia_encrypted_msg
)
print(decrypted_msg.decode("utf-8"))


# user_private_key, user_public_key = RSAHandler.generate_rsa_keys()
# symmetric_key = get_random_bytes(32)
# encrypted_key = RSAHandler.rsa_encrypt(user_public_key, symmetric_key)
