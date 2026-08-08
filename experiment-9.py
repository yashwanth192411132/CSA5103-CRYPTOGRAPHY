# Playfair Cipher Decryption

key = "ROYAL NEW ZEALAND NAVY"

ciphertext = """
KXJEY UREBE ZWEHE WRYTU HEYFS
KREHE GOYFI WTTTU OLKSY CAJPO
BOTEI ZONTX BYBNT GONEY CUZWR
GDSON SXBOU YWRHE BAAHY USEDQ
"""


# Create Playfair matrix
def create_matrix(key):
    key = key.upper().replace(" ", "")
    key = key.replace("J", "I")

    letters = ""

    # Add key letters without repetition
    for ch in key:
        if ch.isalpha() and ch not in letters:
            letters += ch

    # Add remaining alphabet
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in letters:
            letters += ch

    matrix = [letters[i:i+5] for i in range(0, 25, 5)]
    return matrix


# Find position of a letter
def position(matrix, letter):
    if letter == "J":
        letter = "I"

    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col


# Decrypt one pair
def decrypt_pair(matrix, a, b):
    r1, c1 = position(matrix, a)
    r2, c2 = position(matrix, b)

    # Same row
    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + \
               matrix[r2][(c2 - 1) % 5]

    # Same column
    elif c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + \
               matrix[(r2 - 1) % 5][c2]

    # Rectangle rule
    else:
        return matrix[r1][c2] + matrix[r2][c1]


# Create matrix
matrix = create_matrix(key)

print("Playfair Matrix:")
for row in matrix:
    print(" ".join(row))


# Remove spaces from ciphertext
ciphertext = ciphertext.replace(" ", "").replace("\n", "")

# Decrypt
plaintext = ""

for i in range(0, len(ciphertext), 2):
    pair = ciphertext[i:i+2]
    plaintext += decrypt_pair(matrix, pair[0], pair[1])


print("\nDecrypted Message:")
print(plaintext)