# S-DES Encryption and Decryption using Counter (CTR) Mode

# -----------------------------
# S-DES Tables
# -----------------------------

IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]

P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]

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


# -----------------------------
# Utility Functions
# -----------------------------

def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)


def left_shift(bits, n):
    return bits[n:] + bits[:n]


def xor(a, b):
    return ''.join(
        '1' if x != y else '0'
        for x, y in zip(a, b)
    )


# -----------------------------
# Generate S-DES Keys
# -----------------------------

def generate_keys(key):

    key = permute(key, P10)

    left = key[:5]
    right = key[5:]

    # Left shift 1
    left = left_shift(left, 1)
    right = left_shift(right, 1)

    K1 = permute(left + right, P8)

    # Left shift 2
    left = left_shift(left, 2)
    right = left_shift(right, 2)

    K2 = permute(left + right, P8)

    return K1, K2


# -----------------------------
# S-Box
# -----------------------------

def sbox(bits, box):

    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)

    return format(box[row][col], '02b')


# -----------------------------
# F Function
# -----------------------------

def fk(bits, key):

    left = bits[:4]
    right = bits[4:]

    expanded = permute(right, EP)

    xored = xor(expanded, key)

    left_part = xored[:4]
    right_part = xored[4:]

    s0_result = sbox(left_part, S0)
    s1_result = sbox(right_part, S1)

    combined = s0_result + s1_result

    p4_result = permute(combined, P4)

    new_left = xor(left, p4_result)

    return new_left + right


# -----------------------------
# S-DES Encryption
# -----------------------------

def sdes_encrypt(plaintext, key):

    K1, K2 = generate_keys(key)

    # Initial permutation
    bits = permute(plaintext, IP)

    # Round 1
    bits = fk(bits, K1)

    # Switch
    bits = bits[4:] + bits[:4]

    # Round 2
    bits = fk(bits, K2)

    # Inverse permutation
    ciphertext = permute(bits, IP_INV)

    return ciphertext


# -----------------------------
# S-DES Decryption
# -----------------------------

def sdes_decrypt(ciphertext, key):

    K1, K2 = generate_keys(key)

    # Initial permutation
    bits = permute(ciphertext, IP)

    # Round 1 using K2
    bits = fk(bits, K2)

    # Switch
    bits = bits[4:] + bits[:4]

    # Round 2 using K1
    bits = fk(bits, K1)

    # Inverse permutation
    plaintext = permute(bits, IP_INV)

    return plaintext


# -----------------------------
# CTR Mode
# -----------------------------

def ctr_encrypt(plaintext, key, initial_counter):

    ciphertext = ""

    # Divide plaintext into 8-bit blocks
    blocks = [
        plaintext[i:i + 8]
        for i in range(0, len(plaintext), 8)
    ]

    for i, block in enumerate(blocks):

        # Generate counter
        counter = initial_counter + i

        # Convert counter to 8-bit binary
        counter_bits = format(counter, '08b')

        # Encrypt counter
        keystream = sdes_encrypt(counter_bits, key)

        # XOR plaintext with keystream
        encrypted_block = xor(block, keystream)

        ciphertext += encrypted_block

    return ciphertext


# In CTR mode, encryption and decryption
# use exactly the same operation.

def ctr_decrypt(ciphertext, key, initial_counter):

    return ctr_encrypt(ciphertext, key, initial_counter)


# -----------------------------
# Main Program
# -----------------------------

key = "0111111101"

initial_counter = 0

plaintext = "000000010000001000000100"

print("========== S-DES CTR MODE ==========")

print("\nKey       :", key)
print("Counter   :", format(initial_counter, '08b'))

print("Plaintext :", end=" ")

for i in range(0, len(plaintext), 8):
    print(plaintext[i:i + 8], end=" ")

print()


# Encryption
ciphertext = ctr_encrypt(
    plaintext,
    key,
    initial_counter
)

print("\nCiphertext:", end=" ")

for i in range(0, len(ciphertext), 8):
    print(ciphertext[i:i + 8], end=" ")

print()


# Decryption
decrypted = ctr_decrypt(
    ciphertext,
    key,
    initial_counter
)

print("Decrypted :", end=" ")

for i in range(0, len(decrypted), 8):
    print(decrypted[i:i + 8], end=" ")

print()


# Verification
if decrypted == plaintext:
    print("\nDecryption successful!")
else:
    print("\nDecryption failed!")