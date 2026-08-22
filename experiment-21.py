from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# AES block size = 16 bytes
BLOCK_SIZE = 16


# -------------------------------
# Padding and Unpadding
# -------------------------------
def pad(data):
    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)

    # Always add padding, even if data is already
    # an exact multiple of BLOCK_SIZE
    padding = bytes([padding_length]) * padding_length

    return data + padding


def unpad(data):
    padding_length = data[-1]

    if padding_length < 1 or padding_length > BLOCK_SIZE:
        raise ValueError("Invalid padding")

    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Invalid padding")

    return data[:-padding_length]


# -------------------------------
# ECB Mode
# -------------------------------
def ecb_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(plaintext)
    return cipher.encrypt(padded_text)


def ecb_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return unpad(plaintext)


# -------------------------------
# CBC Mode
# -------------------------------
def cbc_encrypt(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plaintext)

    return cipher.encrypt(padded_text)


def cbc_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    return unpad(plaintext)


# -------------------------------
# CFB Mode
# -------------------------------
def cfb_encrypt(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    return cipher.encrypt(plaintext)


def cfb_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    return cipher.decrypt(ciphertext)


# -------------------------------
# Main Program
# -------------------------------
key = get_random_bytes(16)
iv = get_random_bytes(16)

plaintext = b"Hello, this is a secret message!"

print("Original Plaintext:")
print(plaintext.decode())

# ECB
ecb_ciphertext = ecb_encrypt(plaintext, key)
ecb_plaintext = ecb_decrypt(ecb_ciphertext, key)

print("\n--- ECB MODE ---")
print("Encrypted:", ecb_ciphertext.hex())
print("Decrypted:", ecb_plaintext.decode())

# CBC
cbc_ciphertext = cbc_encrypt(plaintext, key, iv)
cbc_plaintext = cbc_decrypt(cbc_ciphertext, key, iv)

print("\n--- CBC MODE ---")
print("Encrypted:", cbc_ciphertext.hex())
print("Decrypted:", cbc_plaintext.decode())

# CFB
cfb_ciphertext = cfb_encrypt(plaintext, key, iv)
cfb_plaintext = cfb_decrypt(cfb_ciphertext, key, iv)

print("\n--- CFB MODE ---")
print("Encrypted:", cfb_ciphertext.hex())
print("Decrypted:", cfb_plaintext.decode())