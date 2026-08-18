def otp_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "").lower()

    ciphertext = ""

    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - ord('a')
        c = (p + key[i]) % 26
        ciphertext += chr(c + ord('a'))

    return ciphertext


def otp_decrypt(ciphertext, key):
    plaintext = ""

    for i in range(len(ciphertext)):
        c = ord(ciphertext[i]) - ord('a')
        p = (c - key[i]) % 26
        plaintext += chr(p + ord('a'))

    return plaintext


# Part (a)
plaintext = "send more money"

key = [9, 0, 1, 7, 23, 15, 21, 14, 11, 11, 2, 8, 9]

ciphertext = otp_encrypt(plaintext, key)

print("Plaintext :", plaintext)
print("Key       :", key)
print("Ciphertext:", ciphertext)


# Part (b)
new_plaintext = "cash not needed"

new_plaintext = new_plaintext.replace(" ", "").lower()

# Find key:
# K = (C - P) mod 26
new_key = []

for i in range(len(ciphertext)):
    c = ord(ciphertext[i]) - ord('a')
    p = ord(new_plaintext[i]) - ord('a')

    k = (c - p) % 26
    new_key.append(k)

print("\nNew plaintext :", new_plaintext)
print("New key       :", new_key)

# Verify
print("Decrypted     :", otp_decrypt(ciphertext, new_key))