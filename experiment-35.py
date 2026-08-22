# One-Time Pad Version of Vigenere Cipher

import random
import string


# -----------------------------------------
# Generate random OTP key
# -----------------------------------------

def generate_key(length):
    return [random.randint(0, 25) for _ in range(length)]


# -----------------------------------------
# Encryption
# -----------------------------------------

def encrypt(plaintext, key):

    ciphertext = ""

    for i, char in enumerate(plaintext):

        if char.isalpha():

            # Convert A-Z to 0-25
            p = ord(char.upper()) - ord('A')

            # Vigenere / OTP encryption
            c = (p + key[i]) % 26

            # Convert back to letter
            ciphertext += chr(c + ord('A'))

    return ciphertext


# -----------------------------------------
# Decryption
# -----------------------------------------

def decrypt(ciphertext, key):

    plaintext = ""

    for i, char in enumerate(ciphertext):

        # Convert A-Z to 0-25
        c = ord(char.upper()) - ord('A')

        # Vigenere / OTP decryption
        p = (c - key[i]) % 26

        # Convert back to letter
        plaintext += chr(p + ord('A'))

    return plaintext


# -----------------------------------------
# Main Program
# -----------------------------------------

print("===== ONE-TIME PAD VIGENERE CIPHER =====")

plaintext = input("Enter plaintext: ").upper()

# Generate random key
key = generate_key(len(plaintext))

print("\nPlaintext:")
print(plaintext)

print("\nRandom Key:")
print(key)


# Encryption
ciphertext = encrypt(plaintext, key)

print("\nEncrypted Ciphertext:")
print(ciphertext)


# Decryption
decrypted = decrypt(ciphertext, key)

print("\nDecrypted Plaintext:")
print(decrypted)


# Verification
if decrypted == plaintext:
    print("\nEncryption and Decryption Successful!")
else:
    print("\nOperation Failed!")