import string

def caesar_encrypt(text, shift):
    """Encrypts text using caesar cipher with given shift (0-25). """
    result = ""
    for char in text:
        if char.isalpha():
            alpha = string.ascii_uppercase
            #find the position in the alphabet and shift
            pos = alpha.index(char.upper())
            newPos = (pos + shift) % 26 #wrap around using modulo giving remainder
            newChar = alpha[newPos]
            #preserve the case
            result += newChar if char.isupper() else newChar.lower()
        else:
            result += char #non-alphabetic characters are unchanged
    return result

def caesar_decrypt(text, shift):
    """Decrypts text using caesar cipher with given shift (0-25). """
    return caesar_encrypt(text, -shift)  # Decryption is just encryption with negative shift

plain= "Hello, World!"
shift=3
encrypted= caesar_encrypt(plain, shift)
print("Encrypted:", encrypted)  # Output: Khoor, Zruog!
print(caesar_decrypt(encrypted, shift))  # Output: Hello, World!