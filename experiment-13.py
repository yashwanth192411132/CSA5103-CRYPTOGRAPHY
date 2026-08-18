import numpy as np

MOD = 26

# Convert letters to numbers
def text_to_numbers(text):
    return [ord(c.lower()) - ord('a') for c in text if c.isalpha()]


# Find modular inverse
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


# Find inverse of a 2x2 matrix modulo 26
def matrix_inverse_2x2(matrix):
    a, b = matrix[0]
    c, d = matrix[1]

    determinant = (a * d - b * c) % MOD

    inv_det = mod_inverse(determinant, MOD)

    if inv_det is None:
        raise ValueError("Matrix has no inverse modulo 26")

    inverse = np.array([
        [d, -b],
        [-c, a]
    ])

    inverse = (inv_det * inverse) % MOD

    return inverse


# ------------------------------------------------
# Known plaintext attack
# ------------------------------------------------

# Suppose we know:
# Plaintext blocks: ME and ET
# Ciphertext blocks: UK and IX

plaintext = "meet"
ciphertext = "ukix"

p = text_to_numbers(plaintext)
c = text_to_numbers(ciphertext)

# Construct plaintext matrix
P = np.array([
    [p[0], p[2]],
    [p[1], p[3]]
])

# Construct ciphertext matrix
C = np.array([
    [c[0], c[2]],
    [c[1], c[3]]
])

print("Plaintext Matrix P:")
print(P)

print("\nCiphertext Matrix C:")
print(C)

# Calculate inverse of P
P_inv = matrix_inverse_2x2(P)

print("\nP inverse modulo 26:")
print(P_inv)

# K = C * P^-1 mod 26
K = (C @ P_inv) % MOD

print("\nRecovered Key Matrix K:")
print(K)

# Convert key matrix into readable form
print("\nRecovered Key:")
print(K)