# RSA Character-by-Character Attack
# Demonstrates why encrypting each alphabetic
# character separately is NOT secure.


# -----------------------------------------
# RSA Encryption
# -----------------------------------------

def rsa_encrypt(message, e, n):
    return pow(message, e, n)


# -----------------------------------------
# Create Codebook
# -----------------------------------------

def create_codebook(e, n):

    codebook = {}

    for value in range(26):

        ciphertext = rsa_encrypt(value, e, n)

        codebook[ciphertext] = value

    return codebook


# -----------------------------------------
# Encrypt Message Character by Character
# -----------------------------------------

def encrypt_text(text, e, n):

    ciphertext = []

    for char in text.upper():

        if char.isalpha():

            value = ord(char) - ord('A')

            encrypted = rsa_encrypt(value, e, n)

            ciphertext.append(encrypted)

    return ciphertext


# -----------------------------------------
# Attack and Recover Plaintext
# -----------------------------------------

def crack_rsa(ciphertext, e, n):

    codebook = create_codebook(e, n)

    plaintext = ""

    for block in ciphertext:

        if block in codebook:

            value = codebook[block]

            plaintext += chr(value + ord('A'))

        else:

            plaintext += "?"

    return plaintext


# -----------------------------------------
# Main Program
# -----------------------------------------

print("===== RSA CHARACTER-BY-CHARACTER ATTACK =====")

# Demonstration RSA values
# In a real system n would be extremely large.

p = 61
q = 53

n = p * q
phi = (p - 1) * (q - 1)

e = 17

message = "HELLO"


print("\nPublic Key:")
print("e =", e)
print("n =", n)

print("\nOriginal Message:")
print(message)


# Encrypt each character separately
ciphertext = encrypt_text(message, e, n)

print("\nEncrypted blocks:")
print(ciphertext)


# Create attack codebook
print("\nBuilding codebook...")

codebook = create_codebook(e, n)

print("Codebook created for 26 possible characters.")


# Recover plaintext
recovered = crack_rsa(ciphertext, e, n)

print("\nRecovered Message:")
print(recovered)