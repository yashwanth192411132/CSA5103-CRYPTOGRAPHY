# Simple Substitution Cipher - Decryption
# The Gold-Bug Cipher

ciphertext = """53‡‡†305))6*;4826)4‡.)4‡);806*;48†8¶60))85;;]8*;:‡*8†83*
*(88)5*†;46(;88*96*?;8)*‡(;485);5*†2:*‡(;4956*2(5*—4)8¶8*
;4069285);)6†8)4‡‡;1(‡9;48081;8:8‡1;48†85;4)485†528806*81(‡9;48;(88;4(‡?34;48)4‡;161;:188;‡?;"""

# Substitution mapping
mapping = {
    '5': 'a',
    '3': 'g',
    '‡': 'o',
    '†': 'd',
    '0': 'l',
    '9': 'r',
    ')': 's',
    '6': 'i',
    '*': 'n',
    ';': 't',
    '4': 'h',
    '8': 'e',
    '2': 'v',
    '(': 'f',
    '1': 'm',
    ':': 'u',
    '?': 'p',
    '¶': 'y',
    '.': 'c',
    '—': 'x',
    ']': 'b'
}

plaintext = ""

for char in ciphertext:
    if char in mapping:
        plaintext += mapping[char]
    else:
        plaintext += char

print("Decrypted Message:")
print(plaintext)