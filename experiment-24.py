# RSA Key Generation Program

# Given public key
e = 31
n = 3599


# --------------------------------
# Find p and q by trial and error
# --------------------------------

p = 0
q = 0

for i in range(2, int(n ** 0.5) + 1):
    if n % i == 0:
        p = i
        q = n // i
        break

print("Public key:")
print("e =", e)
print("n =", n)

print("\nFactors:")
print("p =", p)
print("q =", q)


# --------------------------------
# Calculate Euler's Totient
# --------------------------------

phi = (p - 1) * (q - 1)

print("\nEuler's Totient:")
print("phi(n) =", phi)


# --------------------------------
# Extended Euclidean Algorithm
# --------------------------------

def extended_gcd(a, b):

    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y


# Find multiplicative inverse of e modulo phi
gcd, x, y = extended_gcd(e, phi)

if gcd != 1:
    print("Private key does not exist.")
else:

    # Make the inverse positive
    d = x % phi

    print("\nPrivate key:")
    print("d =", d)
    print("n =", n)

    print("\nPrivate key = (", d, ",", n, ")")

    # Verification
    print("\nVerification:")
    print("(e × d) mod phi(n) =",
          (e * d) % phi)