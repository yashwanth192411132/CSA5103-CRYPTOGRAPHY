import string

def affine_decrypt(ciphertext, a=3, b=15):
    plaintext = ""

    # Find modular inverse of a
    a_inv = pow(a, -1, 26)

    for ch in ciphertext:
        if ch.isalpha():
            # Convert A-Z to 0-25
            y = ord(ch.upper()) - ord('A')

            # Decryption formula
            x = (a_inv * (y - b)) % 26

            plaintext += chr(x + ord('A'))
        else:
            plaintext += ch

    return plaintext


# Input ciphertext
ciphertext = input("Enter the ciphertext: ")

plaintext = affine_decrypt(ciphertext)

print("\nDecrypted plaintext:")
print(plaintext)