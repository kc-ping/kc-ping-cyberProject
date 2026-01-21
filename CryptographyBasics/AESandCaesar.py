import string
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import string
import os,argparse

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


#parser coomand-line arguments (using argparse for a claer CLI)
parser = argparse.ArgumentParser(description="Encrypt or decrypt text using Caesar cipher or AES.")
parser.add_argument('--mode', choices=['encrypt', 'decrypt'], required=True, help="Mode: encrypt or decrypt")
parser.add_argument('--cipher', choices=['caesar', 'aes'], required=True, help="Cipher: caesar or aes")
parser.add_argument('--input', required=True, help="Input text (for caesar) or input filename (for aes)")
parser.add_argument('--output', help="Output filename(optional for (optional))")
parser.add_argument('--key', required=True, help="Shift (0-25) for caesar or passphrase for aes")
args = parser.parse_args()

if os.path.isfile(args.input):
    with open(args.input, 'rb') as f:
        inputData = f.read()
else:
    inputData = args.input.encode('utf-8')

if args.cipher == 'caesar':
    # for caesar, interpret key as interger shift
    shift = int(args.key) % 26
    text= inputData.decode('utf-8')
    if args.mode == 'encrypt':
        result = caesar_encrypt(text, shift)
    else:
        result = caesar_decrypt(text, shift)
    resultData =result.encode('utf-8')

elif args.cipher == 'aes':
    passphrase = args.key.encode('utf-8')
    if args.mode == 'encrypt':
        resultData = aes_encrypt(inputData, passphrase)
    else:
        try:
            resultData = aes_decrypt(inputData, passphrase)
        except (ValueError, KeyError):
            # common cause: wrong passphrase or corrupted input
            print("ERROR: Decryption failed — wrong key/passphrase or corrupted input.", file=sys.stderr)
            sys.exit(2)

if args.output:
    with open(args.output, 'wb') as f:
        f.write(resultData)

else:
    #if output file notgiven , print text for caesar of hex for aes
    if args.cipher == 'caesar':
        print(resultData.decode('utf-8'))
    else:
        #base64 encode for readable output
        import base64
        print(base64.b64encode(resultData).decode('utf-8'))