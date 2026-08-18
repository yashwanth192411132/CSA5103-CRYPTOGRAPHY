from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Generate AES key and IV
key = get_random_bytes(16)
iv = get_random_bytes(16)

message = b"This is a test message for CBC mode error propagation."

# ---------------- ECB MODE ----------------
ecb_cipher = AES.new(key, AES.MODE_ECB)

padded_message = pad(message, AES.block_size)

ecb_ciphertext = ecb_cipher.encrypt(padded_message)

# Introduce an error in one ciphertext block
ecb_corrupted = bytearray(ecb_ciphertext)
ecb_corrupted[16] ^= 1       # Error in second block

# Decrypt corrupted ciphertext
ecb_decrypt = AES.new(key, AES.MODE_ECB)
ecb_plaintext = ecb_decrypt.decrypt(bytes(ecb_corrupted))

print("ECB MODE")
print("--------")
print("Original Ciphertext :", ecb_ciphertext.hex())
print("Corrupted Ciphertext:", bytes(ecb_corrupted).hex())
print("Decrypted Data      :", ecb_plaintext)


# ---------------- CBC MODE ----------------
cbc_cipher = AES.new(key, AES.MODE_CBC, iv)
cbc_ciphertext = cbc_cipher.encrypt(padded_message)

# Introduce an error in C1
cbc_corrupted = bytearray(cbc_ciphertext)
cbc_corrupted[0] ^= 1

# Decrypt corrupted ciphertext
cbc_decrypt = AES.new(key, AES.MODE_CBC, iv)
cbc_plaintext = cbc_decrypt.decrypt(bytes(cbc_corrupted))

print("\nCBC MODE")
print("--------")
print("Original Ciphertext :", cbc_ciphertext.hex())
print("Corrupted Ciphertext:", bytes(cbc_corrupted).hex())
print("Decrypted Data      :", cbc_plaintext)