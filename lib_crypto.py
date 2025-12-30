from Crypto.Cipher import AES, DES
import base64

def _pad(data, block_size):
    while len(data) % block_size != 0:
        data += b" "
    return data

# ========= AES =========
def lib_aes_encrypt(msg, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    padded = _pad(msg.encode(), 16)
    return base64.b64encode(cipher.encrypt(padded)).decode()

def lib_aes_decrypt(msg, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(msg))
    return decrypted.decode().strip()

# ========= DES =========
def lib_des_encrypt(msg, key):
    cipher = DES.new(key.encode(), DES.MODE_ECB)
    padded = _pad(msg.encode(), 8)
    return base64.b64encode(cipher.encrypt(padded)).decode()

def lib_des_decrypt(msg, key):
    cipher = DES.new(key.encode(), DES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(msg))
    return decrypted.decode().strip()
