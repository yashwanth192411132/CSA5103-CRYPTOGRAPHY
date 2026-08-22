# Affine Caesar Cipher
# Encryption: C = (a*p + b) mod 26
# Decryption: P = a^-1 * (C - b) mod 26


from math import gcd


# -----------------------------------------
# Find Multiplicative Inverse
# -----------------------------------------

def mod_inverse(a, m):

    for i in range(1, m):

        if (a * i) % m == 1:
            return i

    return None


# -----------------------------------------
# Encryption
# -----------------------------------------

def encrypt(plaintext, a, b):

    ciphertext = ""

    for char in plaintext.upper():

        if char.isalpha():

            # A = 0, B = 1, ..., Z = 25
            p = ord(char) - ord('A')

            # Affine encryption
            c = (a * p + b) % 26

            ciphertext += chr(c + ord('A'))

        else:
            ciphertext += char

    return ciphertext


# -----------------------------------------
# Decryption
# -----------------------------------------

def decrypt(ciphertext, a, b):

    # Find inverse of a modulo 26
    a_inverse = mod_inverse(a, 26)

    if a_inverse is None:
        return "Invalid value of a"

    plaintext = ""

    for char in ciphertext.upper():

        if char.isalpha():

            # A = 0, B = 1, ..., Z = 25
            c = ord(char) - ord('A')

            # Affine decryption
            p = (a_inverse * (c - b)) % 26

            plaintext += chr(p + ord('A'))

        else:
            plaintext += char

    return plaintext


# -----------------------------------------
# Main Program
# -----------------------------------------

print("========== AFFINE CAESAR CIPHER ==========")

plaintext = input("Enter plaintext: ")

a = int(input("Enter value of a: "))
b = int(input("Enter value of b: "))


# Check whether a is valid
if gcd(a, 26) != 1:

    print("\nInvalid value of a!")
    print("a must be relatively prime to 26.")

else:

    print("\nEncryption formula:")
    print("C = (a*p + b) mod 26")

    # Encryption
    ciphertext = encrypt(
        plaintext,
        a,
        b
    )

    print("\nPlaintext : ", plaintext)
    print("Ciphertext: ", ciphertext)

    # Decryption
    decrypted = decrypt(
        ciphertext,
        a,
        b
    )

    print("Decrypted : ", decrypted)

    if decrypted.upper() == plaintext.upper():
        print("\nEncryption and Decryption Successful!")