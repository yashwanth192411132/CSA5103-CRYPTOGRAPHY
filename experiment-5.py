# Affine Caesar Cipher Encryption

def affine_encrypt(text, a, b):
    # Check if 'a' is valid
    if a not in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
        print("Invalid value of a!")
        return

    result = ""

    for ch in text:
        if ch.isalpha():
            x = ord(ch.upper()) - ord('A')   # Convert A-Z to 0-25
            c = (a * x + b) % 26             # Encryption formula
            result += chr(c + ord('A'))
        else:
            result += ch

    return result


# Main Program
text = input("Enter Plain Text: ")
a = int(input("Enter value of a: "))
b = int(input("Enter value of b: "))

cipher = affine_encrypt(text, a, b)

if cipher:
    print("Cipher Text:", cipher)