# Letter Frequency Attack on Additive Cipher

# English letter frequencies
english_freq = {
    'a': 0.0812, 'b': 0.0149, 'c': 0.0271,
    'd': 0.0432, 'e': 0.1202, 'f': 0.0230,
    'g': 0.0203, 'h': 0.0592, 'i': 0.0731,
    'j': 0.0010, 'k': 0.0069, 'l': 0.0398,
    'm': 0.0261, 'n': 0.0695, 'o': 0.0768,
    'p': 0.0182, 'q': 0.0011, 'r': 0.0602,
    's': 0.0628, 't': 0.0910, 'u': 0.0288,
    'v': 0.0111, 'w': 0.0209, 'x': 0.0017,
    'y': 0.0211, 'z': 0.0007
}


# Decrypt additive cipher
def decrypt(ciphertext, key):
    plaintext = ""

    for ch in ciphertext:
        if ch.isalpha():
            c = ord(ch.lower()) - ord('a')

            # P = (C - K) mod 26
            p = (c - key) % 26

            plaintext += chr(p + ord('a'))
        else:
            plaintext += ch

    return plaintext


# Calculate chi-square score
def frequency_score(text):
    letters = [c for c in text.lower() if c.isalpha()]

    total = len(letters)

    if total == 0:
        return float('inf')

    score = 0

    for letter in english_freq:
        observed = letters.count(letter)
        expected = english_freq[letter] * total

        if expected > 0:
            score += ((observed - expected) ** 2) / expected

    return score


# Get top N possible plaintexts
def frequency_attack(ciphertext, n):
    results = []

    # Try every possible key
    for key in range(26):

        plaintext = decrypt(ciphertext, key)

        score = frequency_score(plaintext)

        results.append((score, key, plaintext))

    # Smaller chi-square score = more likely English
    results.sort()

    return results[:n]


# -------------------------------
# Main Program
# -------------------------------

ciphertext = input("Enter ciphertext: ")

n = int(input("How many possible plaintexts do you want? "))

if n < 1:
    print("Enter a number greater than 0.")

elif n > 26:
    print("Maximum possible results are 26.")

else:
    results = frequency_attack(ciphertext, n)

    print("\nPossible plaintexts in order of likelihood:\n")

    for rank, (score, key, plaintext) in enumerate(results, start=1):

        print(f"{rank}. Key = {key:2d} | "
              f"Score = {score:.2f} | "
              f"Plaintext = {plaintext}")