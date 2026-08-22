import string
import math
import random


# ---------------------------------------------------------
# English letter frequency
# ---------------------------------------------------------

ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51,
    'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09,
    'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23,
    'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.49,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}


# ---------------------------------------------------------
# Common English words
# ---------------------------------------------------------

COMMON_WORDS = {
    "THE": 10,
    "AND": 9,
    "THAT": 8,
    "HAVE": 8,
    "FOR": 7,
    "NOT": 7,
    "WITH": 7,
    "YOU": 7,
    "THIS": 7,
    "BUT": 6,
    "HIS": 6,
    "FROM": 6,
    "THEY": 6,
    "SHE": 6,
    "WHICH": 6,
    "OR": 5,
    "ONE": 5,
    "WE": 5,
    "ALL": 5,
    "WOULD": 5,
    "THERE": 5,
    "THEIR": 5,
    "BE": 5,
    "WAS": 5,
    "ARE": 5,
    "AS": 5,
    "OF": 10,
    "TO": 10,
    "IN": 9,
    "IS": 9
}


# ---------------------------------------------------------
# Calculate letter-frequency score
# ---------------------------------------------------------

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
        return 0

    score = 0

    for letter in string.ascii_uppercase:

        actual = counts[letter] / total * 100
        expected = ENGLISH_FREQ[letter]

        # Smaller difference = better
        score -= abs(actual - expected)

    return score


# ---------------------------------------------------------
# Common-word score
# ---------------------------------------------------------

def word_score(text):

    words = text.upper().split()

    score = 0

    for word in words:

        if word in COMMON_WORDS:
            score += COMMON_WORDS[word]

    return score


# ---------------------------------------------------------
# Combined English score
# ---------------------------------------------------------

def score_text(text):

    return frequency_score(text) + word_score(text) * 2


# ---------------------------------------------------------
# Apply substitution key
# ---------------------------------------------------------

def decrypt_with_key(ciphertext, key):

    plaintext = ""

    for char in ciphertext:

        if char.upper() in key:

            decoded = key[char.upper()]

            if char.islower():
                decoded = decoded.lower()

            plaintext += decoded

        else:
            plaintext += char

    return plaintext


# ---------------------------------------------------------
# Generate random substitution key
# ---------------------------------------------------------

def random_key():

    letters = list(string.ascii_uppercase)

    shuffled = letters[:]

    random.shuffle(shuffled)

    return dict(zip(letters, shuffled))


# ---------------------------------------------------------
# Mutation of substitution key
# ---------------------------------------------------------

def mutate_key(key):

    new_key = key.copy()

    a, b = random.sample(string.ascii_uppercase, 2)

    new_key[a], new_key[b] = new_key[b], new_key[a]

    return new_key


# ---------------------------------------------------------
# Frequency-based initial key
# ---------------------------------------------------------

def frequency_key(ciphertext):

    counts = {
        letter: 0
        for letter in string.ascii_uppercase
    }

    for char in ciphertext.upper():

        if char in counts:
            counts[char] += 1

    cipher_order = sorted(
        counts,
        key=counts.get,
        reverse=True
    )

    english_order = sorted(
        ENGLISH_FREQ,
        key=ENGLISH_FREQ.get,
        reverse=True
    )

    return dict(
        zip(cipher_order, english_order)
    )


# ---------------------------------------------------------
# Hill-climbing attack
# ---------------------------------------------------------

def attack(ciphertext, iterations=30000):

    best_results = []

    # Start with frequency-analysis key
    initial = frequency_key(ciphertext)

    current_key = initial
    current_plaintext = decrypt_with_key(
        ciphertext,
        current_key
    )

    current_score = score_text(current_plaintext)

    best_results.append(
        (current_score, current_plaintext)
    )

    # Multiple random restarts
    for restart in range(20):

        if restart == 0:
            key = initial
        else:
            key = random_key()

        plaintext = decrypt_with_key(
            ciphertext,
            key
        )

        score = score_text(plaintext)

        for _ in range(iterations // 20):

            new_key = mutate_key(key)

            new_plaintext = decrypt_with_key(
                ciphertext,
                new_key
            )

            new_score = score_text(new_plaintext)

            if new_score > score:

                key = new_key
                score = new_score

                best_results.append(
                    (score, new_plaintext)
                )

    # Remove duplicate plaintexts
    unique = {}

    for score, plaintext in best_results:

        if plaintext not in unique:
            unique[plaintext] = score
        elif score > unique[plaintext]:
            unique[plaintext] = score

    # Sort from most likely to least likely
    results = sorted(
        unique.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return results


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

print("==============================================")
print(" MONOALPHABETIC SUBSTITUTION CIPHER ATTACK")
print("==============================================")

ciphertext = input(
    "\nEnter ciphertext:\n"
)

top_n = int(
    input(
        "\nHow many possible plaintexts do you want? "
    )
)


print("\nAnalyzing ciphertext...")
print("Please wait...\n")


results = attack(ciphertext)


print("========== POSSIBLE PLAINTEXTS ==========")


for i, (plaintext, score) in enumerate(
        results[:top_n], start=1):

    print(
        f"\n{i}. Score = {score:.2f}"
    )

    print(
        plaintext
    )


print("\n==========================================")
print("Attack completed.")