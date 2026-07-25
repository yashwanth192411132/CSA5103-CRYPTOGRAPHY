plain = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cipher = "QWERTYUIOPASDFGHJKLZXCVBNM"

text = input("Enter encrypted text: ").upper()

result = ""

for ch in text:
    if ch.isalpha():
        result += plain[cipher.index(ch)]
    else:
        result += ch

print("Decrypted Text:", result)