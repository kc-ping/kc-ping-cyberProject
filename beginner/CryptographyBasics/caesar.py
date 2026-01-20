import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad


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


def aes_encrypt(plaintext, password):
    """ Encrypts plaintext using AES encryption with the given password. """
    # convert password to bytes and generate a random salt
    salt= get_random_bytes(16)
    # Derive a 32-byte(256-bit) AES key from the password
    key = PBKDF2(password, salt, dkLen=32, count=1000000)# high iteration count for security
    # Create random 16-byte IV
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Pad plaintext to be multiple of block size (16 bytes for AES)
    ciphertext= cipher.encrypt(pad(plaintext, AES.block_size))
    # Return salt + iv + ciphertext for use in decryption
    return salt + iv + ciphertext

def aes_decrypt(ciphertext, password):
    """ Decrypts ciphertext using AES decryption with the given password. """
    # Extract salt, (first 16 bytes), iv (next 16 bytes), and actual ciphertext
    salt = ciphertext[:16]
    iv = ciphertext[16:32]
    actual_ciphertext = ciphertext[32:]
    # Derive the same AES key from the password and salt
    key = PBKDF2(password, salt, dkLen=32,count=1000000)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt and unpad the plaintext
    plaintext = unpad(cipher.decrypt(actual_ciphertext), AES.block_size)

    return plaintext


data = b"Secret message"
password = "my_strong_passphrase"
cipher_blob = aes_encrypt(data, password)
print(cipher_blob.hex())  # (binary output; in a real tool you might base64-encode it)

# Later, to decrypt:
decrypted = aes_decrypt(cipher_blob, password)
print(decrypted)  # b"Secret message"
