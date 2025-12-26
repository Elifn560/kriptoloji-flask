import requests
from Crypto.Cipher import AES, DES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from manual_crypto import manual_aes_encrypt, manual_des_encrypt
from server import public_key  # Sunucunun public key'i

AES_KEY = b'16byteslongkey!!'
DES_KEY = b'8bytesk'

def pad_bytes(data, block_size):
    while len(data) % block_size != 0:
        data += b' '
    return data

# --- Library Encrypt ---
def encrypt_aes(msg):
    from Crypto.Cipher import AES
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad_bytes(msg.encode(), 16))).decode()

def encrypt_des(msg):
    from Crypto.Cipher import DES
    cipher = DES.new(DES_KEY, DES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad_bytes(msg.encode(), 8))).decode()

def encrypt_rsa(msg):
    cipher = PKCS1_OAEP.new(public_key)
    return base64.b64encode(cipher.encrypt(msg.encode())).decode()

# --- Kullanıcı Girişi ---
msg = input("Enter message: ")
alg = input("Choose algorithm (AES/DES/RSA): ")
mode = input("Choose mode (library/manual): ")

if mode == 'library':
    if alg == 'AES':
        encrypted_msg = encrypt_aes(msg)
    elif alg == 'DES':
        encrypted_msg = encrypt_des(msg)
    elif alg == 'RSA':
        encrypted_msg = encrypt_rsa(msg)
    else:
        print("Unsupported algorithm")
        exit()
elif mode == 'manual':
    if alg == 'AES':
        encrypted_msg = manual_aes_encrypt(msg)
    elif alg == 'DES':
        encrypted_msg = manual_des_encrypt(msg)
    else:
        print("Manual mode supports only AES/DES")
        exit()
else:
    print("Invalid mode")
    exit()

# --- Sunucuya Gönder ---
response = requests.post('http://127.0.0.1:5000/send', json={
    "algorithm": alg,
    "mode": mode,
    "message": encrypted_msg
})

print(response.json())
