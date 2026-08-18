from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

# 3DES requires a 16 or 24 byte key
key = DES3.adjust_key_parity(get_random_bytes(24))

# CBC requires an 8-byte IV for 3DES
iv = get_random_bytes(8)

# Message to encrypt
message = input("Enter the message: ").encode()

# Create 3DES CBC cipher
cipher = DES3.new(key, DES3.MODE_CBC, iv)

# Pad message because 3DES has an 8-byte block size
padded_message = pad(message, DES3.block_size)

# Encrypt
ciphertext = cipher.encrypt(padded_message)

print("\n3DES CBC Encryption")
print("-------------------")
print("Key       :", key.hex())
print("IV        :", iv.hex())
print("Plaintext :", message.decode())
print("Ciphertext:", ciphertext.hex())