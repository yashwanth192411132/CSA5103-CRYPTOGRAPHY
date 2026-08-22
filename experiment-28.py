# Diffie-Hellman Protocol
# Comparison of a^x and x^a

# ---------------------------------------
# Normal Diffie-Hellman
# ---------------------------------------

def normal_diffie_hellman(q, a, alice_secret, bob_secret):

    # Alice sends a^xA mod q
    A = pow(a, alice_secret, q)

    # Bob sends a^xB mod q
    B = pow(a, bob_secret, q)

    # Shared key
    alice_key = pow(B, alice_secret, q)
    bob_key = pow(A, bob_secret, q)

    return A, B, alice_key, bob_key


# ---------------------------------------
# Modified Protocol: x^a mod q
# ---------------------------------------

def modified_protocol(q, a, alice_secret, bob_secret):

    # Alice sends xA^a mod q
    A = pow(alice_secret, a, q)

    # Bob sends xB^a mod q
    B = pow(bob_secret, a, q)

    # Alice uses Bob's value and her secret
    alice_key = pow(B, alice_secret, q)

    # Bob uses Alice's value and his secret
    bob_key = pow(A, bob_secret, q)

    return A, B, alice_key, bob_key


# ---------------------------------------
# Eve recovers the secret number
# ---------------------------------------

def eve_recover_secret(public_value, a, q):

    # Fermat's theorem: exponents operate modulo q-1
    # Find inverse of a modulo q-1

    inverse_a = pow(a, -1, q - 1)

    secret = pow(public_value, inverse_a, q)

    return secret


# ---------------------------------------
# Main Program
# ---------------------------------------

q = 23
a = 5

alice_secret = 6
bob_secret = 15


print("========== NORMAL DIFFIE-HELLMAN ==========")

A, B, alice_key, bob_key = normal_diffie_hellman(
    q, a, alice_secret, bob_secret
)

print("Public prime q =", q)
print("Public number a =", a)

print("\nAlice secret =", alice_secret)
print("Bob secret   =", bob_secret)

print("\nAlice sends:", A)
print("Bob sends  :", B)

print("\nAlice shared key:", alice_key)
print("Bob shared key  :", bob_key)

if alice_key == bob_key:
    print("Key agreement successful!")


print("\n========== MODIFIED x^a PROTOCOL ==========")

A, B, alice_key, bob_key = modified_protocol(
    q, a, alice_secret, bob_secret
)

print("Alice sends xA^a mod q =", A)
print("Bob sends xB^a mod q   =", B)

print("\nAlice shared key:", alice_key)
print("Bob shared key  :", bob_key)

if alice_key == bob_key:
    print("Key agreement successful!")


print("\n========== EVE'S ATTACK ==========")

print("Eve knows:")
print("q =", q)
print("a =", a)
print("Alice public value =", A)
print("Bob public value   =", B)

# Recover Alice's secret
recovered_alice = eve_recover_secret(A, a, q)

# Recover Bob's secret
recovered_bob = eve_recover_secret(B, a, q)

print("\nEve recovered Alice's secret:", recovered_alice)
print("Eve recovered Bob's secret  :", recovered_bob)

# Eve calculates shared key
eve_key = pow(B, recovered_alice, q)

print("\nEve's calculated key:", eve_key)

if eve_key == alice_key:
    print("Eve successfully broke the system!")