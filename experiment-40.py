import string
import random
import math


# ============================================================
# English letter frequencies
# ============================================================

ENGLISH_FREQ = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25,
    'E': 12.70, 'F': 2.23, 'G': 2.02, 'H': 6.09,
    'I': 6.97, 'J': 0.15, 'K': 0.77, 'L': 4.03,
    'M': 2.41, 'N': 6.75, 'O': 7.51, 'P': 1.93,
    'Q': 0.10, 'R': 5.99, 'S': 6.33, 'T': 9.06,
    'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15,
    'Y': 1.97, 'Z': 0.07
}


# ============================================================
# Common English patterns
# ============================================================

COMMON_BIGRAMS = {
    "TH": 5, "HE": 5, "IN": 4, "ER": 4, "AN": 4,
    "RE": 4, "ON": 4, "AT": 3, "EN": 3, "ND": 3,
    "TI": 3, "ES": 3, "OR": 3, "TE": 3, "OF": 3,
    "ED": 3, "IS": 3, "IT": 3, "AL": 3, "AR": 3,
    "ST": 3, "TO": 4, "NT": 2, "NG": 2, "SE": 2,
    "HA": 2, "AS": 2, "OU": 2, "IO": 2, "LE": 2
}


COMMON_TRIGRAMS = {
    "THE": 10, "AND": 8, "ING": 8, "HER": 6,
    "ERE": 5, "ENT": 6, "THA": 5, "NTH": 5,
    "WAS": 5, "ETH": 5, "FOR": 5, "DTH": 4,
    "HES": 4, "VER": 4, "EST": 4, "HIS": 4,
    "OFT": 3, "STH": 3, "OTH": 3, "RES": 3,
    "ATI": 3, "ALL": 3, "TER": 3, "CON": 3
}


COMMON_WORDS = {
    "THE": 15,
    "OF": 12,
    "AND": 12,
    "TO": 12,
    "IN": 11,
    "A": 10,
    "IS": 10,
    "THAT": 10,
    "FOR": 9,
    "IT": 9,
    "AS": 9,
    "WAS": 9,
    "WITH": 9,
    "BE": 8,
    "BY": 8,
    "ON": 8,
    "NOT": 8,
    "HE": 8,
    "I": 8,
    "THIS": 8,
    "ARE": 8,
    "OR": 7,
    "HIS": 7,
    "FROM": 7,
    "BUT": 7,
    "HAVE": 7,
    "THEY": 7,
    "YOU": 7,
    "ONE": 6,
    "ALL": 6,
    "WE": 6,
    "CAN": 6,
    "HER": 6,
    "HAS": 6,
    "WERE": 6,
    "THERE": 6,
    "THEIR": 6,
    "WHAT": 5,
    "WHEN": 5,
    "WHO": 5,
    "WHICH": 5,
    "WILL": 5,
    "WOULD": 5,
    "ABOUT": 5
}


# ============================================================
# Decrypt using substitution key
#
# key[cipher_letter] = plaintext_letter
# ============================================================

def decrypt(ciphertext, key):

    plaintext = ""

    for char in ciphertext:

        upper = char.upper()

        if upper in key:

            decoded = key[upper]

            if char.islower():
                decoded = decoded.lower()

            plaintext += decoded

        else:
            plaintext += char

    return plaintext


# ============================================================
# Score plaintext
# ============================================================

def score_text(text):

    text = ''.join(
        c for c in text.upper()
        if c.isalpha()
    )

    score = 0

    # --------------------------------------------------------
    # Letter-frequency score
    # --------------------------------------------------------

    if len(text) > 0:

        counts = {
            c: text.count(c)
            for c in string.ascii_uppercase
        }

        total = len(text)

        for letter in string.ascii_uppercase:

            actual = counts[letter] / total * 100
            expected = ENGLISH_FREQ[letter]

            score -= abs(actual - expected) * 0.15

    # --------------------------------------------------------
    # Bigram score
    # --------------------------------------------------------

    for i in range(len(text) - 1):

        pair = text[i:i + 2]

        if pair in COMMON_BIGRAMS:
            score += COMMON_BIGRAMS[pair]

    # --------------------------------------------------------
    # Trigram score
    # --------------------------------------------------------

    for i in range(len(text) - 2):

        triple = text[i:i + 3]

        if triple in COMMON_TRIGRAMS:
            score += COMMON_TRIGRAMS[triple] * 2

    # --------------------------------------------------------
    # Word score
    # --------------------------------------------------------

    words = text.split()

    # The text above has spaces removed, so use a second
    # scoring pass on the original text.
    return score


def complete_score(text):

    score = score_text(text)

    words = text.upper().split()

    for word in words:

        if word in COMMON_WORDS:
            score += COMMON_WORDS[word] * 5

    return score


# ============================================================
# Create random substitution key
# ============================================================

def random_key():

    cipher_letters = list(string.ascii_uppercase)
    plain_letters = list(string.ascii_uppercase)

    random.shuffle(plain_letters)

    return dict(
        zip(cipher_letters, plain_letters)
    )


# ============================================================
# Mutate key by swapping two plaintext mappings
# ============================================================

def mutate_key(key):

    new_key = key.copy()

    a, b = random.sample(
        string.ascii_uppercase,
        2
    )

    new_key[a], new_key[b] = (
        new_key[b],
        new_key[a]
    )

    return new_key


# ============================================================
# Hill-climbing / simulated annealing
# ============================================================

def solve_cipher(ciphertext, iterations=20000):

    key = random_key()

    plaintext = decrypt(
        ciphertext,
        key
    )

    current_score = complete_score(
        plaintext
    )

    best_key = key.copy()
    best_score = current_score

    temperature = 20.0

    for i in range(iterations):

        new_key = mutate_key(key)

        new_plaintext = decrypt(
            ciphertext,
            new_key
        )

        new_score = complete_score(
            new_plaintext
        )

        difference = new_score - current_score

        # Accept better keys
        # Sometimes accept worse keys to escape local maxima.
        if (
            difference > 0
            or random.random() < math.exp(
                difference / max(temperature, 0.01)
            )
        ):

            key = new_key
            current_score = new_score

        if current_score > best_score:

            best_score = current_score
            best_key = key.copy()

        # Gradually reduce temperature
        temperature *= 0.9997

    best_plaintext = decrypt(
        ciphertext,
        best_key
    )

    return best_score, best_plaintext


# ============================================================
# Automatic frequency attack
# ============================================================

def frequency_attack(ciphertext, top_n):

    candidates = []

    # Multiple independent attacks
    # increase the chance of finding a good solution.

    restarts = 30

    for run in range(restarts):

        score, plaintext = solve_cipher(
            ciphertext,
            iterations=15000
        )

        candidates.append(
            (score, plaintext)
        )

    # Remove duplicate plaintexts
    unique = {}

    for score, plaintext in candidates:

        if plaintext not in unique:
            unique[plaintext] = score

        elif score > unique[plaintext]:
            unique[plaintext] = score

    # Sort from most likely to least likely
    ranked = sorted(
        unique.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:top_n]


# ============================================================
# Main Program
# ============================================================

print("=" * 60)
print(" AUTOMATIC MONOALPHABETIC SUBSTITUTION CIPHER ATTACK")
print("=" * 60)

ciphertext = input(
    "\nEnter ciphertext:\n"
)

top_n = int(
    input(
        "\nHow many possible plaintexts do you want? "
    )
)

if top_n < 1:
    top_n = 1

print("\nPerforming automatic cryptanalysis...")
print("Please wait...\n")

results = frequency_attack(
    ciphertext,
    top_n
)


# ============================================================
# Display results
# ============================================================

print("=" * 60)
print(" POSSIBLE PLAINTEXTS")
print("=" * 60)

for number, (score, plaintext) in enumerate(
        results,
        start=1):

    print(
        f"\n{number}. Score = {score:.2f}"
    )

    print(
        "   " + plaintext
    )

print("\n" + "=" * 60)
print("Attack completed.")
print("=" * 60)