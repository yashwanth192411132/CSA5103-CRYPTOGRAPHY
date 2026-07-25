# Vigenere Cipher (Polyalphabetic Substitution)

plaintext = input("Enter Plaintext: ").upper()
key = input("Enter Key: ").upper()

cipher = ""
key_index = 0

for ch in plaintext:
    if ch.isalpha():
        p = ord(ch) - ord('A')
        k = ord(key[key_index % len(key)]) - ord('A')

        c = (p + k) % 26
        cipher += chr(c + ord('A'))

        key_index += 1
    else:
        cipher += ch

print("Encrypted Text:", cipher)