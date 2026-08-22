from math import gcd


# -----------------------------------------
# Extended Euclidean Algorithm
# -----------------------------------------
def extended_gcd(a, b):

    if b == 0:
        return a, 1, 0

    g, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return g, x, y


# -----------------------------------------
# Modular Inverse
# -----------------------------------------
def mod_inverse(e, phi):

    g, x, y = extended_gcd(e, phi)

    if g != 1:
        return None

    return x % phi


# -----------------------------------------
# RSA Common Factor Attack
# -----------------------------------------

print("===== RSA COMMON FACTOR ATTACK =====")

n = int(input("Enter n: "))
e = int(input("Enter public key e: "))
message = int(input("Enter plaintext block: "))


# Find common factor
common_factor = gcd(message, n)

print("\nGCD(message, n) =", common_factor)


# Check whether useful factor exists
if common_factor == 1 or common_factor == n:

    print("\nNo useful common factor was found.")
    print("The plaintext block does not help factor n.")

else:

    # Recover p and q
    p = common_factor
    q = n // p

    print("\nFactorization found:")
    print("p =", p)
    print("q =", q)

    # Calculate Euler's Totient
    phi = (p - 1) * (q - 1)

    print("\nEuler's Totient:")
    print("phi(n) =", phi)

    # Calculate private key
    d = mod_inverse(e, phi)

    if d is None:

        print("\nPrivate key cannot be calculated.")

    else:

        print("\nPrivate key:")
        print("d =", d)
        print("n =", n)

        print("\nPrivate Key = (", d, ",", n, ")")

        # Verification
        print("\nVerification:")
        print("(e × d) mod phi(n) =",
              (e * d) % phi)