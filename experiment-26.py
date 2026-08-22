import math
import random


# ---------------------------------------
# Greatest Common Divisor
# ---------------------------------------
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# ---------------------------------------
# Extended Euclidean Algorithm
# ---------------------------------------
def extended_gcd(a, b):

    if b == 0:
        return a, 1, 0

    g, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return g, x, y


# ---------------------------------------
# Modular Inverse
# ---------------------------------------
def mod_inverse(e, phi):

    g, x, y = extended_gcd(e, phi)

    if g != 1:
        return None

    return x % phi


# ---------------------------------------
# Simple Prime Check
# ---------------------------------------
def is_prime(n):

    if n < 2:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True


# ---------------------------------------
# Generate RSA Key Pair
# ---------------------------------------
def generate_keypair():

    # Small primes for demonstration
    primes = [
        101, 103, 107, 109,
        113, 127, 131, 137
    ]

    p = random.choice(primes)
    q = random.choice(primes)

    while q == p:
        q = random.choice(primes)

    n = p * q

    phi = (p - 1) * (q - 1)

    # Choose e
    e = 65537

    if gcd(e, phi) != 1:
        e = 3

        while gcd(e, phi) != 1:
            e += 2

    # Calculate d
    d = mod_inverse(e, phi)

    return p, q, n, e, d


# ---------------------------------------
# RSA Encryption
# ---------------------------------------
def encrypt(message, e, n):
    return pow(message, e, n)


# ---------------------------------------
# RSA Decryption
# ---------------------------------------
def decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)


# =======================================
# Main Program
# =======================================

print("===== RSA KEY REGENERATION TEST =====")


# Original RSA key pair
p, q, n, e, d = generate_keypair()

print("\nOriginal RSA Keys")
print("-----------------")
print("p =", p)
print("q =", q)
print("n =", n)
print("e =", e)
print("d =", d)


# Simulate private-key leakage
print("\nBob's private key has been leaked!")
print("Leaked d =", d)


# ------------------------------------------------
# UNSAFE METHOD:
# Keep the same n and generate a new e and d
# ------------------------------------------------

print("\n--- Unsafe: Same Modulus ---")

new_e = 3

phi = (p - 1) * (q - 1)

while gcd(new_e, phi) != 1:
    new_e += 2

new_d = mod_inverse(new_e, phi)

print("Old n =", n)
print("New e =", new_e)
print("New d =", new_d)

print("\nThe modulus n has NOT changed.")
print("Therefore, this is NOT a safe solution.")


# ------------------------------------------------
# SAFE METHOD:
# Generate completely new RSA key pair
# ------------------------------------------------

print("\n--- Safe: New RSA Key Pair ---")

p2, q2, n2, e2, d2 = generate_keypair()

print("New p =", p2)
print("New q =", q2)
print("New n =", n2)
print("New e =", e2)
print("New d =", d2)

print("\nNew modulus generated!")
print("Bob now has a completely new RSA key pair.")