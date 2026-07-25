# Caesar Cipher Encryption and Decryption

def caesar_cipher(text, key, mode):
    result = ""

    for char in text:
        if char.isalpha():
            # Handle uppercase and lowercase letters
            start = ord('A') if char.isupper() else ord('a')

            if mode == "encrypt":
                shifted = (ord(char) - start + key) % 26
            elif mode == "decrypt":
                shifted = (ord(char) - start - key) % 26

            result += chr(start + shifted)
        else:
            # Keep spaces, numbers, and symbols unchanged
            result += char

    return result


# Main Program
text = input("Enter the message: ")
key = int(input("Enter the key (1-25): "))

if key < 1 or key > 25:
    print("Invalid key! Key must be between 1 and 25.")
else:
    choice = input("Type 'encrypt' or 'decrypt': ").lower()

    if choice == "encrypt":
        print("Encrypted Message:", caesar_cipher(text, key, "encrypt"))
    elif choice == "decrypt":
        print("Decrypted Message:", caesar_cipher(text, key, "decrypt"))
    else:
        print("Invalid choice!")