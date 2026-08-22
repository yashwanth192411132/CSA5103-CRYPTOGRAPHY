# DSA vs RSA Signature Demonstration
#
# DSA:
#   Same message -> different signatures
#   because a new random k is generated.
#
# RSA PKCS#1 v1.5:
#   Same message -> same signature
#   because the signing operation is deterministic.

from Crypto.PublicKey import DSA, RSA
from Crypto.Signature import DSS, pkcs1_15
from Crypto.Hash import SHA256


# ==========================================================
# DSA SIGNATURE
# ==========================================================

print("========== DSA SIGNATURE ==========")

# Generate DSA key
dsa_key = DSA.generate(2048)

# Create signer
dsa_signer = DSS.new(dsa_key, 'fips-186-3')

message = b"Hello World"

# First DSA signature
hash1 = SHA256.new(message)
signature1 = dsa_signer.sign(hash1)

# Second DSA signature
hash2 = SHA256.new(message)
signature2 = dsa_signer.sign(hash2)

print("\nMessage:")
print(message.decode())

print("\nDSA Signature 1:")
print(signature1.hex())

print("\nDSA Signature 2:")
print(signature2.hex())

if signature1 != signature2:
    print("\nDSA result:")
    print("The two signatures are DIFFERENT.")
else:
    print("\nDSA result:")
    print("The signatures are SAME.")


# ==========================================================
# RSA SIGNATURE
# ==========================================================

print("\n\n========== RSA SIGNATURE ==========")

# Generate RSA key
rsa_key = RSA.generate(2048)

# First RSA signature
hash3 = SHA256.new(message)
rsa_signature1 = pkcs1_15.new(rsa_key).sign(hash3)

# Second RSA signature
hash4 = SHA256.new(message)
rsa_signature2 = pkcs1_15.new(rsa_key).sign(hash4)

print("\nMessage:")
print(message.decode())

print("\nRSA Signature 1:")
print(rsa_signature1.hex())

print("\nRSA Signature 2:")
print(rsa_signature2.hex())

if rsa_signature1 == rsa_signature2:
    print("\nRSA result:")
    print("The two signatures are SAME.")
else:
    print("\nRSA result:")
    print("The signatures are DIFFERENT.")


# ==========================================================
# FINAL COMPARISON
# ==========================================================

print("\n\n========== COMPARISON ==========")

print("DSA : Same message -> Different signatures")
print("RSA : Same message -> Same signatures")