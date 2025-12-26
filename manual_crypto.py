from Crypto.Cipher import AES, DES
import base64

AES_KEY = b'16byteslongkey!!'
DES_KEY = b'8bytesk'

def manual_aes_encrypt(text):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    padded = text.encode()
    while len(padded) % 16 != 0:
        padded += b' '
    return base64.b64encode(cipher.encrypt(padded)).decode()

def manual_aes_decrypt(cipher_text):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(cipher_text))
    return decrypted.decode().strip()

def manual_des_encrypt(text):
    cipher = DES.new(DES_KEY, DES.MODE_ECB)
    padded = text.encode()
    while len(padded) % 8 != 0:
        padded += b' '
    return base64.b64encode(cipher.encrypt(padded)).decode()

def manual_des_decrypt(cipher_text):
    cipher = DES.new(DES_KEY, DES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(cipher_text))
    return decrypted.decode().strip()
