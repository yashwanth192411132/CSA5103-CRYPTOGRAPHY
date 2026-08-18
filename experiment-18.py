# DES Key Generation
# First 24 bits of each subkey come from C (28 bits)
# Second 24 bits come from D (28 bits)

# PC-1 table
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# PC-2 table
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# DES left shift schedule
SHIFT_SCHEDULE = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]


def permute(key, table):
    """Perform permutation using the given table."""
    return ''.join(key[i - 1] for i in table)


def left_shift(bits, shifts):
    """Perform circular left shift."""
    return bits[shifts:] + bits[:shifts]


def generate_subkeys(key):
    # Step 1: Apply PC-1
    permuted_key = permute(key, PC1)

    # Step 2: Split into two 28-bit halves
    C = permuted_key[:28]
    D = permuted_key[28:]

    subkeys = []

    # Step 3: Generate 16 subkeys
    for round_no in range(16):

        # Shift C and D
        C = left_shift(C, SHIFT_SCHEDULE[round_no])
        D = left_shift(D, SHIFT_SCHEDULE[round_no])

        # First 24 bits come from C
        C24 = permute(C, PC2[:24])

        # Second 24 bits come from D
        D24 = permute(D, [x - 28 for x in PC2[24:]])

        # Combine both 24-bit parts
        subkey = C24 + D24

        subkeys.append(subkey)

    return subkeys


# Example 64-bit DES key
key = "133457799BBCDFF1"

# Convert hexadecimal key to binary
key_binary = bin(int(key, 16))[2:].zfill(64)

# Generate subkeys
subkeys = generate_subkeys(key_binary)

print("DES 16 Subkeys")
print("=" * 60)

for i, subkey in enumerate(subkeys, 1):
    print(f"K{i} = {subkey}")
    print(f"     First 24 bits : {subkey[:24]}")
    print(f"     Second 24 bits: {subkey[24:]}")
    print()