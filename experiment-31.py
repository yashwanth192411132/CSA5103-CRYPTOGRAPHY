from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# -----------------------------------------
# Left Shift and Conditional XOR
# -----------------------------------------

def left_shift_one(bit_string, block_size):
    """
    Left shift a block by one bit.
    If the most significant bit was 1,
    XOR with the CMAC reduction constant.
    """

    # Check MSB
    msb = bit_string[0]

    # Convert binary string to integer
    value = int(bit_string, 2)

    # Left shift
    value = (value << 1) & ((1 << block_size) - 1)

    # CMAC reduction constants
    if block_size == 64:
        Rb = 0x1B

    elif block_size == 128:
        Rb = 0x87

    else:
        raise ValueError("Unsupported block size")

    # Conditional XOR
    if msb == '1':
        value ^= Rb

    return format(value, '0{}b'.format(block_size))


# -----------------------------------------
# Generate CMAC Subkeys
# -----------------------------------------

def generate_subkeys(key, block_size=128):

    # AES uses 128-bit blocks
    if block_size == 128:

        cipher = AES.new(key, AES.MODE_ECB)

    else:
        raise ValueError(
            "This demonstration uses AES (128-bit block)"
        )

    # Zero block
    zero_block = bytes(block_size // 8)

    # L = E(K, 0^n)
    L_bytes = cipher.encrypt(zero_block)

    L = bin(int.from_bytes(L_bytes, 'big'))[2:].zfill(block_size)

    # Generate K1
    K1 = left_shift_one(L, block_size)

    # Generate K2
    K2 = left_shift_one(K1, block_size)

    return L, K1, K2


# -----------------------------------------
# Main Program
# -----------------------------------------

key = get_random_bytes(16)

L, K1, K2 = generate_subkeys(key, 128)


print("========== CMAC SUBKEY GENERATION ==========")

print("\nBlock size:")
print("128 bits")

print("\nCMAC Constant Rb:")
print("0x87")

print("\nL = E(K, 0^128):")
print(L)

print("\nK1:")
print(K1)

print("\nK2:")
print(K2)