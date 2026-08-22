# S-DES Encryption/Decryption using CBC Mode

# Initial Permutation
IP = [2, 6, 3, 1, 4, 8, 5, 7]

# Inverse Initial Permutation
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

# Expansion/Permutation
EP = [4, 1, 2, 3, 2, 3, 4, 1]

# P4
P4 = [2, 4, 3, 1]

# P10
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]

# P8
P8 = [6, 3, 7, 4, 8, 5, 10, 9]

# S-Boxes
S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]


# -------------------------------------------------
# Utility Functions
# -------------------------------------------------

def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)


def left_shift(bits, n):
    return bits[n:] + bits[:n]


def xor(a, b):
    return ''.join('1' if x != y else '0'
                   for x, y in zip(a, b))


# -------------------------------------------------
# Key Generation
# -------------------------------------------------

def generate_keys(key):
    # P10
    key = permute(key, P10)

    left = key[:5]
    right = key[5:]

    # LS-1
    left = left_shift(left, 1)
    right = left_shift(right, 1)

    k1 = permute(left + right, P8)

    # LS-2
    left = left_shift(left, 2)
    right = left_shift(right, 2)

    k2 = permute(left + right, P8)

    return k1, k2


# -------------------------------------------------
# S-Box Function
# -------------------------------------------------

def sbox(bits, box):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)

    value = box[row][col]

    return format(value, '02b')


# -------------------------------------------------
# F Function
# -------------------------------------------------

def fk(bits, key):
    left = bits[:4]
    right = bits[4:]

    expanded = permute(right, EP)

    xored = xor(expanded, key)

    left4 = xored[:4]
    right4 = xored[4:]

    s0_output = sbox(left4, S0)
    s1_output = sbox(right4, S1)

    p4_input = s0_output + s1_output
    p4_output = permute(p4_input, P4)

    new_left = xor(left, p4_output)

    return new_left + right


# -------------------------------------------------
# S-DES Encryption
# -------------------------------------------------

def sdes_encrypt(plaintext, key):
    k1, k2 = generate_keys(key)

    # Initial permutation
    bits = permute(plaintext, IP)

    # Round 1
    bits = fk(bits, k1)

    # Switch
    bits = bits[4:] + bits[:4]

    # Round 2
    bits = fk(bits, k2)

    # Inverse permutation
    ciphertext = permute(bits, IP_INV)

    return ciphertext


# -------------------------------------------------
# S-DES Decryption
# -------------------------------------------------

def sdes_decrypt(ciphertext, key):
    k1, k2 = generate_keys(key)

    # Initial permutation
    bits = permute(ciphertext, IP)

    # Round 1 with K2
    bits = fk(bits, k2)

    # Switch
    bits = bits[4:] + bits[:4]

    # Round 2 with K1
    bits = fk(bits, k1)

    # Inverse permutation
    plaintext = permute(bits, IP_INV)

    return plaintext


# -------------------------------------------------
# CBC Encryption
# -------------------------------------------------

def cbc_encrypt(plaintext, key, iv):
    ciphertext = ""
    previous = iv

    # Divide plaintext into 8-bit blocks
    blocks = [
        plaintext[i:i+8]
        for i in range(0, len(plaintext), 8)
    ]

    for block in blocks:

        # CBC: XOR plaintext block with previous ciphertext
        xored = xor(block, previous)

        encrypted = sdes_encrypt(xored, key)

        ciphertext += encrypted

        previous = encrypted

    return ciphertext


# -------------------------------------------------
# CBC Decryption
# -------------------------------------------------

def cbc_decrypt(ciphertext, key, iv):
    plaintext = ""
    previous = iv

    blocks = [
        ciphertext[i:i+8]
        for i in range(0, len(ciphertext), 8)
    ]

    for block in blocks:

        decrypted = sdes_decrypt(block, key)

        # CBC: XOR decrypted block with previous ciphertext
        original = xor(decrypted, previous)

        plaintext += original

        previous = block

    return plaintext


# -------------------------------------------------
# Main Program
# -------------------------------------------------

key = "0111111101"
iv = "10101010"

plaintext = "0000000100100011"

print("========== S-DES CBC MODE ==========")

print("\nKey        :", key)
print("IV         :", iv)
print("Plaintext  :", plaintext)

# Encryption
ciphertext = cbc_encrypt(plaintext, key, iv)

print("\nEncrypted  :", ciphertext)

# Decryption
decrypted = cbc_decrypt(ciphertext, key, iv)

print("Decrypted  :", decrypted)

# Verification
if decrypted == plaintext:
    print("\nDecryption successful!")
else:
    print("\nDecryption failed!")