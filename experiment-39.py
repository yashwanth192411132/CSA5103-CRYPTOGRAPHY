# ==========================================
# ADDITIVE CIPHER - LETTER FREQUENCY ATTACK
# ==========================================

import string


# ------------------------------------------
# English letter frequencies
# ------------------------------------------

ENGLISH_FREQ = {
    'A': 8.17,
    'B': 1.49,
    'C': 2.78,
    'D': 4.25,
    'E': 12.70,
    'F': 2.23,
    'G': 2.02,
    'H': 6.09,
    'I': 6.97,
    'J': 0.15,
    'K': 0.77,
    'L': 4.03,
    'M': 2.41,
    'N': 6.75,
    'O': 7.51,
    'P': 1.93,
    'Q': 0.10,
    'R': 5.99,
    'S': 6.33,
    'T': 9.06,
    'U': 2.76,
    'V': 0.98,
    'W': 2.36,
    'X': 0.15,
    'Y': 1.97,
    'Z': 0.07
}


# ------------------------------------------
# Decrypt additive cipher
# ------------------------------------------

def decrypt(ciphertext, key):

    plaintext = ""

    for char in ciphertext:

        if char.isalpha():

            c = ord(char.upper()) - ord('A')

            # P = (C - key) mod 26
            p = (c - key) % 26

            plaintext += chr(p + ord('A'))

        else:
            plaintext += char

    return plaintext


# ------------------------------------------
# Calculate frequency score
# ------------------------------------------

def frequency_score(text):

    counts = {
        letter: 0
        for letter in string.ascii_uppercase
    }

    total = 0

    for char in text:

        if char.isalpha():

            counts[char.upper()] += 1
            total += 1

    if total == 0:
        return float('-inf')

    score = 0

    for letter in string.ascii_uppercase:

        actual_frequency = (
            counts[letter] / total
        ) * 100

        expected_frequency = ENGLISH_FREQ[letter]

        # Lower difference = better
        score -= abs(
            actual_frequency - expected_frequency
        )

    return score


# ------------------------------------------
# Frequency attack
# ------------------------------------------

def frequency_attack(ciphertext, top_n):

    results = []

    # Try all 26 possible keys
    for key in range(26):

        plaintext = decrypt(
            ciphertext,
            key
        )

        score = frequency_score(
            plaintext
        )

        results.append(
            (score, key, plaintext)
        )

    # Sort from most likely to least likely
    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return results[:top_n]


# ------------------------------------------
# Main Program
# ------------------------------------------

print("==========================================")
print("     ADDITIVE CIPHER FREQUENCY ATTACK")
print("==========================================")

ciphertext = input(
    "\nEnter ciphertext: "
)

top_n = int(
    input(
        "How many possible plaintexts? "
    )
)

# Make sure top_n is between 1 and 26
top_n = max(1, min(top_n, 26))


print("\nAnalyzing all 26 possible keys...\n")


results = frequency_attack(
    ciphertext,
    top_n
)


# ------------------------------------------
# Display results
# ------------------------------------------

print("========== POSSIBLE PLAINTEXTS ==========")

for position, (score, key, plaintext) in enumerate(
        results, start=1):

    print(
        f"\n{position}. Key = {key}"
    )

    print(
        f"   Score = {score:.2f}"
    )

    print(
        f"   Plaintext = {plaintext}"
    )


print("\n==========================================")
print("Attack completed.")