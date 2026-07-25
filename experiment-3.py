# Playfair Cipher Encryption (Easy Version)

# Function to create 5x5 matrix
def create_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    used = []

    for ch in key:
        if ch.isalpha() and ch not in used:
            used.append(ch)

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # J is omitted
        if ch not in used:
            used.append(ch)

    for i in range(0, 25, 5):
        matrix.append(used[i:i+5])

    return matrix


# Find position of a letter
def find_position(matrix, ch):
    if ch == "J":
        ch = "I"
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j


# Encrypt plaintext
def encrypt(matrix, text):
    text = text.upper().replace("J", "I")
    text = "".join([c for c in text if c.isalpha()])

    pairs = []
    i = 0

    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                pairs.append(a + "X")
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        else:
            pairs.append(a + "X")
            i += 1

    cipher = ""

    for pair in pairs:
        r1, c1 = find_position(matrix, pair[0])
        r2, c2 = find_position(matrix, pair[1])

        # Same row
        if r1 == r2:
            cipher += matrix[r1][(c1 + 1) % 5]
            cipher += matrix[r2][(c2 + 1) % 5]

        # Same column
        elif c1 == c2:
            cipher += matrix[(r1 + 1) % 5][c1]
            cipher += matrix[(r2 + 1) % 5][c2]

        # Rectangle rule
        else:
            cipher += matrix[r1][c2]
            cipher += matrix[r2][c1]

    return cipher


# Main Program
key = input("Enter keyword: ")
plaintext = input("Enter plaintext: ")

matrix = create_matrix(key)

print("\nPlayfair Matrix:")
for row in matrix:
    print(row)

cipher = encrypt(matrix, plaintext)

print("\nEncrypted Text:", cipher)