# ECB, CBC and CFB Modes
# AES block size = 128 bits (16 bytes)

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


BLOCK_SIZE = 16   # 16 bytes = 128 bits


# -------------------------------------------------
# Padding
# 1 bit followed by 0 bits
# -------------------------------------------------

def pad(data):

    # Add a 0x80 byte:
    # 10000000 in binary
    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)

    if padding_length == 0:
        padding_length = BLOCK_SIZE

    padding = b'\x80' + b'\x00' * (padding_length - 1)

    return data + padding


# -------------------------------------------------
# Remove Padding
# -------------------------------------------------

def unpad(data):

    # Remove trailing zeros
    data = data.rstrip(b'\x00')

    # Remove the leading 1 bit
    if data and data[-1:] == b'\x80':
        data = data[:-1]

    return data


# -------------------------------------------------
# ECB Encryption
# -------------------------------------------------

def ecb_encrypt(plaintext, key):

    cipher = AES.new(key, AES.MODE_ECB)

    padded = pad(plaintext)

    return cipher.encrypt(padded)


# -------------------------------------------------
# ECB Decryption
# -------------------------------------------------

def ecb_decrypt(ciphertext, key):

    cipher = AES.new(key, AES.MODE_ECB)

    plaintext = cipher.decrypt(ciphertext)

    return unpad(plaintext)


# -------------------------------------------------
# CBC Encryption
# -------------------------------------------------

def cbc_encrypt(plaintext, key, iv):

    cipher = AES.new(key, AES.MODE_CBC, iv)

    padded = pad(plaintext)

    return cipher.encrypt(padded)


# -------------------------------------------------
# CBC Decryption
# -------------------------------------------------

def cbc_decrypt(ciphertext, key, iv):

    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = cipher.decrypt(ciphertext)

    return unpad(plaintext)


# -------------------------------------------------
# CFB Encryption
# -------------------------------------------------

def cfb_encrypt(plaintext, key, iv):

    # CFB does not require padding when using
    # an appropriate segment size.
    cipher = AES.new(
        key,
        AES.MODE_CFB,
        iv=iv,
        segment_size=128
    )

    return cipher.encrypt(plaintext)


# -------------------------------------------------
# CFB Decryption
# -------------------------------------------------

def cfb_decrypt(ciphertext, key, iv):

    cipher = AES.new(
        key,
        AES.MODE_CFB,
        iv=iv,
        segment_size=128
    )

    return cipher.decrypt(ciphertext)


# =================================================
# MAIN PROGRAM
# =================================================

key = get_random_bytes(16)
iv = get_random_bytes(16)

plaintext = b"Hello, this is a secret message."


print("========== ECB, CBC AND CFB MODES ==========")

print("\nOriginal Plaintext:")
print(plaintext.decode())


# -------------------------------------------------
# ECB
# -------------------------------------------------

ecb_ciphertext = ecb_encrypt(
    plaintext,
    key
)

ecb_plaintext = ecb_decrypt(
    ecb_ciphertext,
    key
)

print("\n----- ECB MODE -----")

print("Encrypted:")
print(ecb_ciphertext.hex())

print("Decrypted:")
print(ecb_plaintext.decode())


# -------------------------------------------------
# CBC
# -------------------------------------------------

cbc_ciphertext = cbc_encrypt(
    plaintext,
    key,
    iv
)

cbc_plaintext = cbc_decrypt(
    cbc_ciphertext,
    key,
    iv
)

print("\n----- CBC MODE -----")

print("Encrypted:")
print(cbc_ciphertext.hex())

print("Decrypted:")
print(cbc_plaintext.decode())


# -------------------------------------------------
# CFB
# -------------------------------------------------

cfb_ciphertext = cfb_encrypt(
    plaintext,
    key,
    iv
)

cfb_plaintext = cfb_decrypt(
    cfb_ciphertext,
    key,
    iv
)

print("\n----- CFB MODE -----")

print("Encrypted:")
print(cfb_ciphertext.hex())

print("Decrypted:")
print(cfb_plaintext.decode())


# -------------------------------------------------
# Verification
# -------------------------------------------------

print("\n========== VERIFICATION ==========")

if ecb_plaintext == plaintext:
    print("ECB : Successful")
else:
    print("ECB : Failed")

if cbc_plaintext == plaintext:
    print("CBC : Successful")
else:
    print("CBC : Failed")

if cfb_plaintext == plaintext:
    print("CFB : Successful")
else:
    print("CFB : Failed")