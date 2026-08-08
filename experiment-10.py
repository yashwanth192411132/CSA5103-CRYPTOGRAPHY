# Playfair Cipher Encryption

matrix = [
    ['M', 'F', 'H', 'I', 'K'],
    ['U', 'N', 'O', 'P', 'Q'],
    ['Z', 'V', 'W', 'X', 'Y'],
    ['E', 'L', 'A', 'R', 'G'],
    ['D', 'S', 'T', 'B', 'C']
]

message = "Must see you over Cadogan West. Coming at once."


# Find position of a letter
def find_position(letter):
    if letter == 'J':
        letter = 'I'

    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col


# Prepare message
def prepare_text(text):
    text = text.upper().replace(" ", "")
    text = text.replace(".", "")

    # J is treated as I
    text = text.replace("J", "I")

    result = ""
    i = 0

    while i < len(text):
        a = text[i]

        if i + 1 < len(text):
            b = text[i + 1]

            if a == b:
                result += a + 'X'
                i += 1
            else:
                result += a + b
                i += 2
        else:
            result += a + 'X'
            i += 1

    return result


# Encrypt two letters
def encrypt_pair(a, b):
    r1, c1 = find_position(a)
    r2, c2 = find_position(b)

    # Same row
    if r1 == r2:
        return (
            matrix[r1][(c1 + 1) % 5] +
            matrix[r2][(c2 + 1) % 5]
        )

    # Same column
    elif c1 == c2:
        return (
            matrix[(r1 + 1) % 5][c1] +
            matrix[(r2 + 1) % 5][c2]
        )

    # Rectangle rule
    else:
        return (
            matrix[r1][c2] +
            matrix[r2][c1]
        )


# Prepare plaintext
prepared = prepare_text(message)

print("Prepared Text:", prepared)

# Encrypt
ciphertext = ""

for i in range(0, len(prepared), 2):
    ciphertext += encrypt_pair(
        prepared[i],
        prepared[i + 1]
    )

print("Encrypted Text:", ciphertext)