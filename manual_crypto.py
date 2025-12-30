# manual_crypto.py
# KÜTÜPHANE KULLANMADAN (EĞİTİM AMAÇLI)

import base64

# =========================
# MANUAL AES (Toy Version)
# =========================

BLOCK_SIZE_AES = 16

def _pad(data, size):
    while len(data) % size != 0:
        data += b" "
    return data

def manual_aes_encrypt(text, key):
    """
    Basitleştirilmiş AES mantığı:
    XOR + blok mantığı (educational)
    """
    data = _pad(text.encode(), BLOCK_SIZE_AES)
    key = key.encode()

    encrypted = bytearray()

    for i in range(len(data)):
        encrypted.append(data[i] ^ key[i % len(key)])

    return base64.b64encode(encrypted).decode()

def manual_aes_decrypt(cipher_text, key):
    data = base64.b64decode(cipher_text)
    key = key.encode()

    decrypted = bytearray()

    for i in range(len(data)):
        decrypted.append(data[i] ^ key[i % len(key)])

    return decrypted.decode().strip()


# =========================
# MANUAL DES (Toy Version)
# =========================

BLOCK_SIZE_DES = 8

def manual_des_encrypt(text, key):
    """
    Basitleştirilmiş DES mantığı:
    XOR + 8 byte blok
    """
    data = _pad(text.encode(), BLOCK_SIZE_DES)
    key = key.encode()

    encrypted = bytearray()

    for i in range(len(data)):
        encrypted.append(data[i] ^ key[i % len(key)])

    return base64.b64encode(encrypted).decode()

def manual_des_decrypt(cipher_text, key):
    data = base64.b64decode(cipher_text)
    key = key.encode()

    decrypted = bytearray()

    for i in range(len(data)):
        decrypted.append(data[i] ^ key[i % len(key)])

    return decrypted.decode().strip()
