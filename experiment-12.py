import numpy as np

# Key matrix
K = np.array([
    [9, 4],
    [5, 7]
])

plaintext = "meet me at the usual place at ten rather than eight oclock"

# Remove spaces
plaintext = ''.join(c for c in plaintext.lower() if c.isalpha())

# Add X if the length is odd
if len(plaintext) % 2 != 0:
    plaintext += 'x'

ciphertext = ""

print("Encryption calculations:\n")

for i in range(0, len(plaintext), 2):

    pair = plaintext[i:i+2]

    # Convert letters to numbers
    P = np.array([
        [ord(pair[0]) - ord('a')],
        [ord(pair[1]) - ord('a')]
    ])

    # C = K * P mod 26
    C = np.dot(K, P) % 26

    encrypted_pair = chr(C[0][0] + ord('a')) + \
                     chr(C[1][0] + ord('a'))

    ciphertext += encrypted_pair

    print(f"{pair.upper()} -> {encrypted_pair.upper()}")

print("\nPlaintext :", plaintext.upper())
print("Ciphertext:", ciphertext.upper())