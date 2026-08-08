import string

def create_cipher_alphabet(keyword):
    keyword = keyword.upper()

    # Remove duplicate letters from keyword
    key = ""
    for ch in keyword:
        if ch.isalpha() and ch not in key:
            key += ch

    # Add remaining unused letters
    for ch in string.ascii_uppercase:
        if ch not in key:
            key += ch

    return key


def encrypt(plaintext, cipher_alphabet):
    alphabet = string.ascii_uppercase
    ciphertext = ""

    for ch in plaintext:
        if ch.isalpha():
            # Preserve lowercase
            index = alphabet.index(ch.upper())
            encrypted = cipher_alphabet[index]

            if ch.islower():
                encrypted = encrypted.lower()

            ciphertext += encrypted
        else:
            ciphertext += ch

    return ciphertext


def decrypt(ciphertext, cipher_alphabet):
    alphabet = string.ascii_uppercase
    plaintext = ""

    for ch in ciphertext:
        if ch.isalpha():
            index = cipher_alphabet.index(ch.upper())
            decrypted = alphabet[index]

            if ch.islower():
                decrypted = decrypted.lower()

            plaintext += decrypted
        else:
            plaintext += ch

    return plaintext


# Keyword
keyword = "CIPHER"

# Create cipher alphabet
cipher_alphabet = create_cipher_alphabet(keyword)

print("Plain : ", string.ascii_uppercase)
print("Cipher: ", cipher_alphabet)

# Input plaintext
plaintext = input("\nEnter plaintext: ")

# Encryption
ciphertext = encrypt(plaintext, cipher_alphabet)

print("Encrypted text:", ciphertext)

# Decryption
decrypted = decrypt(ciphertext, cipher_alphabet)

print("Decrypted text:", decrypted)