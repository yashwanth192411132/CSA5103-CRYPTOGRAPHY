# DES Encryption and Decryption
# Block size : 64 bits
# Effective key size : 56 bits
#
# Install library first:
# pip install pycryptodome

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad


# -----------------------------------------
# DES Encryption
# -----------------------------------------

def encrypt_message(message, key):

    cipher = DES.new(key, DES.MODE_ECB)

    # DES works on 8-byte (64-bit) blocks
    padded_message = pad(message, DES.block_size)

    ciphertext = cipher.encrypt(padded_message)

    return ciphertext


# -----------------------------------------
# DES Decryption
# -----------------------------------------

def decrypt_message(ciphertext, key):

    cipher = DES.new(key, DES.MODE_ECB)

    plaintext = cipher.decrypt(ciphertext)

    # Remove padding
    plaintext = unpad(plaintext, DES.block_size)

    return plaintext


# -----------------------------------------
# Main Program
# -----------------------------------------

print("========== DATA ENCRYPTION STANDARD (DES) ==========")

# DES requires an 8-byte key
key = b"12345678"

# Message
message = b"Hello DES Encryption"


print("\nOriginal Message:")
print(message.decode())


# Encryption
ciphertext = encrypt_message(message, key)

print("\nEncrypted Ciphertext:")
print(ciphertext.hex())


# Decryption
decrypted_message = decrypt_message(ciphertext, key)

print("\nDecrypted Message:")
print(decrypted_message.decode())


# Verification
if decrypted_message == message:
    print("\nEncryption and Decryption Successful!")
else:
    print("\nOperation Failed!")