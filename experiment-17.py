# DES Key Generation for Decryption
# 16 keys are generated in reverse order: K16, K15, ..., K1

# DES left shift schedule used during encryption
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]


def left_shift(bits, n):
    """Perform circular left shift."""
    return bits[n:] + bits[:n]


def right_shift(bits, n):
    """Perform circular right shift."""
    return bits[-n:] + bits[:-n]


def generate_decryption_keys(C, D):
    """
    Generate DES keys for decryption.

    C and D are the 28-bit halves obtained after
    applying PC-1 to the original 64-bit key.
    """

    keys = []

    # Generate encryption keys first
    encryption_keys = []

    c = C
    d = D

    for shift in SHIFT_SCHEDULE:
        c = left_shift(c, shift)
        d = left_shift(d, shift)

        # Combine C and D
        key = c + d
        encryption_keys.append(key)

    # Reverse the encryption keys for decryption
    keys = encryption_keys[::-1]

    return keys


# Example 28-bit C and D values
C = "000110110000001011101111111111"
D = "010101010110100101001001011100"

decryption_keys = generate_decryption_keys(C, D)

print("DES Decryption Keys")
print("-" * 40)

for i, key in enumerate(decryption_keys, start=1):
    # K16 is used first during decryption
    print(f"K{16 - i + 1}: {key}")