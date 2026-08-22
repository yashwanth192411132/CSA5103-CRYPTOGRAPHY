# Hill Cipher Known-Plaintext Attack
#
# C = K * P (mod 26)
#
# If enough plaintext-ciphertext pairs are known,
# the encryption matrix K can be recovered.

import math


MOD = 26


# ---------------------------------------------------------
# Convert letters to numbers
# ---------------------------------------------------------

def text_to_numbers(text):

    return [
        ord(c.upper()) - ord('A')
        for c in text
        if c.isalpha()
    ]


def numbers_to_text(numbers):

    return ''.join(
        chr((n % 26) + ord('A'))
        for n in numbers
    )


# ---------------------------------------------------------
# Matrix multiplication modulo 26
# ---------------------------------------------------------

def matrix_multiply(A, B):

    rows = len(A)
    cols = len(B[0])
    common = len(B)

    result = [
        [0 for _ in range(cols)]
        for _ in range(rows)
    ]

    for i in range(rows):
        for j in range(cols):

            for k in range(common):

                result[i][j] += A[i][k] * B[k][j]

            result[i][j] %= MOD

    return result


# ---------------------------------------------------------
# Modular inverse
# ---------------------------------------------------------

def mod_inverse(a, m):

    for x in range(1, m):

        if (a * x) % m == 1:
            return x

    return None


# ---------------------------------------------------------
# Inverse of 2x2 matrix modulo 26
# ---------------------------------------------------------

def matrix_inverse_2x2(matrix):

    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    d = matrix[1][1]

    determinant = (a * d - b * c) % MOD

    inverse_det = mod_inverse(
        determinant,
        MOD
    )

    if inverse_det is None:
        raise ValueError(
            "Matrix cannot be inverted modulo 26."
        )

    inverse = [
        [
            (d * inverse_det) % MOD,
            (-b * inverse_det) % MOD
        ],
        [
            (-c * inverse_det) % MOD,
            (a * inverse_det) % MOD
        ]
    ]

    return inverse


# ---------------------------------------------------------
# Hill Cipher Encryption
# ---------------------------------------------------------

def hill_encrypt(text, key):

    numbers = text_to_numbers(text)

    # Make length even
    if len(numbers) % 2 != 0:
        numbers.append(23)       # X

    ciphertext = []

    for i in range(0, len(numbers), 2):

        P = [
            [numbers[i]],
            [numbers[i + 1]]
        ]

        C = matrix_multiply(key, P)

        ciphertext.append(C[0][0])
        ciphertext.append(C[1][0])

    return numbers_to_text(ciphertext)


# ---------------------------------------------------------
# Recover Hill Cipher Key
# ---------------------------------------------------------

def recover_key(plaintext, ciphertext):

    P_numbers = text_to_numbers(plaintext)
    C_numbers = text_to_numbers(ciphertext)

    if len(P_numbers) != len(C_numbers):
        raise ValueError(
            "Plaintext and ciphertext lengths must match."
        )

    if len(P_numbers) < 4:
        raise ValueError(
            "At least two plaintext-ciphertext blocks "
            "are required."
        )

    # Use first two plaintext blocks
    #
    # P_matrix =
    # [ P1 P3 ]
    # [ P2 P4 ]

    P_matrix = [
        [P_numbers[0], P_numbers[2]],
        [P_numbers[1], P_numbers[3]]
    ]

    # Corresponding ciphertext matrix
    #
    # C_matrix =
    # [ C1 C3 ]
    # [ C2 C4 ]

    C_matrix = [
        [C_numbers[0], C_numbers[2]],
        [C_numbers[1], C_numbers[3]]
    ]

    # P^-1
    P_inverse = matrix_inverse_2x2(
        P_matrix
    )

    # K = C * P^-1
    K = matrix_multiply(
        C_matrix,
        P_inverse
    )

    return K


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

print("==========================================")
print("     HILL CIPHER KNOWN-PLAINTEXT ATTACK")
print("==========================================")


# Example secret key
original_key = [
    [3, 3],
    [2, 5]
]

print("\nOriginal secret key:")
print(original_key)


# Known plaintext
plaintext = "HELP"

# Generate corresponding ciphertext
ciphertext = hill_encrypt(
    plaintext,
    original_key
)

print("\nKnown plaintext:")
print(plaintext)

print("\nKnown ciphertext:")
print(ciphertext)


# -----------------------------------------
# Attack
# -----------------------------------------

recovered_key = recover_key(
    plaintext,
    ciphertext
)

print("\nRecovered key:")
print(recovered_key)


# -----------------------------------------
# Verify recovered key
# -----------------------------------------

test_message = "MEETME"

encrypted = hill_encrypt(
    test_message,
    recovered_key
)

print("\nTest plaintext:")
print(test_message)

print("\nEncrypted using recovered key:")
print(encrypted)


if recovered_key == original_key:

    print("\nAttack successful!")
    print("The Hill cipher key was recovered.")

else:

    print("\nAttack failed.")