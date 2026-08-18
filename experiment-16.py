import random
import math
import string
from collections import Counter

# -----------------------------------------
# English letter frequency
# -----------------------------------------

ENGLISH_FREQ = {
    'A': 0.0812, 'B': 0.0149, 'C': 0.0271,
    'D': 0.0432, 'E': 0.1202, 'F': 0.0230,
    'G': 0.0203, 'H': 0.0592, 'I': 0.0731,
    'J': 0.0010, 'K': 0.0069, 'L': 0.0398,
    'M': 0.0261, 'N': 0.0695, 'O': 0.0768,
    'P': 0.0182, 'Q': 0.0011, 'R': 0.0602,
    'S': 0.0628, 'T': 0.0910, 'U': 0.0288,
    'V': 0.0111, 'W': 0.0209, 'X': 0.0017,
    'Y': 0.0211, 'Z': 0.0007
}

ALPHABET = string.ascii_uppercase


# -----------------------------------------
# Decrypt using substitution key
# -----------------------------------------

def decrypt(ciphertext, key):
    plaintext = ""

    for ch in ciphertext:
        if ch.upper() in ALPHABET:

            index = ALPHABET.index(ch.upper())
            decrypted = key[index]

            if ch.islower():
                decrypted = decrypted.lower()

            plaintext += decrypted

        else:
            plaintext += ch

    return plaintext


# -----------------------------------------
# Frequency score
# -----------------------------------------

def frequency_score(text):
    letters = [
        c.upper() for c in text
        if c.upper() in ALPHABET
    ]

    if not letters:
        return float("inf")

    total = len(letters)
    counts = Counter(letters)

    score = 0

    for letter in ALPHABET:

        observed = counts[letter]
        expected = ENGLISH_FREQ[letter] * total

        if expected > 0:
            score += ((observed - expected) ** 2) / expected

    return score


# -----------------------------------------
# Common English words
# -----------------------------------------

COMMON_WORDS = {
    "THE", "OF", "AND", "TO", "IN", "A", "IS",
    "THAT", "FOR", "IT", "AS", "WITH", "BE",
    "ON", "BY", "THIS", "ARE", "FROM", "OR",
    "HAVE", "NOT", "BUT", "WHAT", "ALL", "WERE",
    "WHEN", "WE", "THERE", "CAN", "AN", "YOUR"
}


# -----------------------------------------
# Word score
# -----------------------------------------

def word_score(text):
    words = text.upper().split()

    score = 0

    for word in words:
        word = ''.join(c for c in word if c.isalpha())

        if word in COMMON_WORDS:
            score += 10

    return score


# -----------------------------------------
# Combined score
# -----------------------------------------

def score_plaintext(text):
    freq = frequency_score(text)
    words = word_score(text)

    return -freq + words


# -----------------------------------------
# Create random substitution key
# -----------------------------------------

def random_key():
    key = list(ALPHABET)
    random.shuffle(key)

    return key


# -----------------------------------------
# Modify key by swapping two letters
# -----------------------------------------

def mutate_key(key):
    new_key = key.copy()

    a, b = random.sample(range(26), 2)

    new_key[a], new_key[b] = new_key[b], new_key[a]

    return new_key


# -----------------------------------------
# Simulated Annealing
# -----------------------------------------

def attack(ciphertext, iterations=20000):

    key = random_key()

    plaintext = decrypt(ciphertext, key)

    current_score = score_plaintext(plaintext)

    best_key = key.copy()
    best_score = current_score

    temperature = 20.0

    for i in range(iterations):

        new_key = mutate_key(key)

        new_plaintext = decrypt(ciphertext, new_key)

        new_score = score_plaintext(new_plaintext)

        difference = new_score - current_score

        # Accept better solutions
        if difference > 0:

            key = new_key
            current_score = new_score

        # Sometimes accept worse solutions
        else:

            probability = math.exp(
                difference / temperature
            )

            if random.random() < probability:
                key = new_key
                current_score = new_score

        # Save best solution
        if current_score > best_score:

            best_score = current_score
            best_key = key.copy()

        # Gradually reduce temperature
        temperature *= 0.9997

        if temperature < 0.1:
            temperature = 0.1

    return best_key, best_score


# -----------------------------------------
# Main frequency attack
# -----------------------------------------

def frequency_attack(ciphertext, top_n):

    results = []

    # Multiple attempts because substitution
    # cipher has a very large key space.
    for attempt in range(20):

        key, score = attack(ciphertext)

        plaintext = decrypt(ciphertext, key)

        results.append(
            (score, plaintext, key)
        )

    # Remove duplicate plaintexts
    unique = {}

    for score, plaintext, key in results:

        if plaintext not in unique:
            unique[plaintext] = (score, key)

    results = []

    for plaintext, (score, key) in unique.items():

        results.append(
            (score, plaintext, key)
        )

    # Highest score first
    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return results[:top_n]


# -----------------------------------------
# User Interface
# -----------------------------------------

print("==========================================")
print(" Monoalphabetic Substitution Cipher Attack")
print("==========================================")

ciphertext = input(
    "\nEnter ciphertext:\n"
)

top_n = int(
    input(
        "\nHow many possible plaintexts do you want? "
    )
)

if top_n < 1:
    print("Enter a number greater than 0.")

elif top_n > 20:
    print("Maximum recommended value is 20.")

else:

    print(
        "\nAttacking cipher..."
    )

    results = frequency_attack(
        ciphertext,
        top_n
    )

    print(
        "\nPossible plaintexts "
        "in rough order of likelihood:\n"
    )

    for i, (score, plaintext, key) in enumerate(
        results, start=1
    ):

        print(
            f"{i}. Score = {score:.2f}"
        )

        print(
            f"   Plaintext: {plaintext}"
        )

        print()