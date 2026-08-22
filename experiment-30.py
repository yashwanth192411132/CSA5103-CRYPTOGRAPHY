# CBC-MAC Forgery Demonstration
# One-block message X
# Forged two-block message:
# X || (X XOR T)

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


BLOCK_SIZE = 16


# -----------------------------------------
# CBC-MAC for a one-block message
# -----------------------------------------

def cbc_mac_one_block(key, message):
    cipher = AES.new(key, AES.MODE_ECB)

    # CBC-MAC uses IV = 0
    iv = bytes(BLOCK_SIZE)

    # First CBC block:
    # T = E(K, X XOR IV)
    xored = bytes(a ^ b for a, b in zip(message, iv))

    return cipher.encrypt(xored)


# -----------------------------------------
# CBC-MAC for a two-block message
# -----------------------------------------

def cbc_mac_two_blocks(key, block1, block2):
    cipher = AES.new(key, AES.MODE_ECB)

    # IV = 0
    iv = bytes(BLOCK_SIZE)

    # First block
    c1_input = bytes(
        a ^ b for a, b in zip(block1, iv)
    )

    c1 = cipher.encrypt(c1_input)

    # Second block
    c2_input = bytes(
        a ^ b for a, b in zip(block2, c1)
    )

    c2 = cipher.encrypt(c2_input)

    return c2


# -----------------------------------------
# Main Program
# -----------------------------------------

# Secret key known only to the sender/receiver
key = get_random_bytes(16)

# One-block message X
X = b"ABCDEFGHIJKLMNOP"


print("========== CBC-MAC FORGERY ==========")

print("\nOriginal message X:")
print(X)

# -----------------------------------------
# Step 1: Obtain MAC of X
# -----------------------------------------

T = cbc_mac_one_block(key, X)

print("\nMAC of X:")
print(T.hex())


# -----------------------------------------
# Step 2: Construct forged second block
# -----------------------------------------

X_XOR_T = bytes(
    a ^ b for a, b in zip(X, T)
)

print("\nX XOR T:")
print(X_XOR_T.hex())


# -----------------------------------------
# Step 3: Construct forged message
# -----------------------------------------

print("\nForged two-block message:")
print("X || (X XOR T)")

# Calculate MAC of forged message
forged_mac = cbc_mac_two_blocks(
    key,
    X,
    X_XOR_T
)

print("\nMAC of forged message:")
print(forged_mac.hex())


# -----------------------------------------
# Verification
# -----------------------------------------

if forged_mac == T:
    print("\nAttack successful!")
    print("MAC(X) = MAC(X || (X XOR T))")
else:
    print("\nAttack failed!")