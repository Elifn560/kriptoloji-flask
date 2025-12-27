

import string


def caesar_encrypt(text, key):
    key = int(key)
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((ord(ch) - base + key) % 26 + base)
        else:
            result += ch
    return result

def caesar_decrypt(text, key):
    return caesar_encrypt(text, -int(key))



def vigenere_encrypt(text, key):
    key = key.lower()
    res = ""
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[ki % len(key)]) - ord('a')
            res += chr((ord(ch) - base + shift) % 26 + base)
            ki += 1
        else:
            res += ch
    return res

def vigenere_decrypt(text, key):
    key = key.lower()
    res = ""
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[ki % len(key)]) - ord('a')
            res += chr((ord(ch) - base - shift) % 26 + base)
            ki += 1
        else:
            res += ch
    return res



def rot_encrypt(text, key):
    return caesar_encrypt(text, int(key))

def rot_decrypt(text, key):
    return caesar_decrypt(text, int(key))



def affine_encrypt(text, key):
    a, b = map(int, key.split(","))
    res = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            res += chr(((a * (ord(ch) - base) + b) % 26) + base)
        else:
            res += ch
    return res

def affine_decrypt(text, key):
    a, b = map(int, key.split(","))
    a_inv = pow(a, -1, 26)
    res = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            res += chr((a_inv * ((ord(ch) - base) - b) % 26) + base)
        else:
            res += ch
    return res


def substitution_encrypt(text, key):
    alphabet = string.ascii_lowercase
    mapping = {alphabet[i]: key[i] for i in range(26)}
    res = ""
    for ch in text.lower():
        res += mapping[ch] if ch in mapping else ch
    return res

def substitution_decrypt(text, key):
    alphabet = string.ascii_lowercase
    reverse = {key[i]: alphabet[i] for i in range(26)}
    res = ""
    for ch in text.lower():
        res += reverse[ch] if ch in reverse else ch
    return res



MANUAL_ALGORITHMS = {
    "caesar": {
        "encrypt": caesar_encrypt,
        "decrypt": caesar_decrypt
    },
    "vigenere": {
        "encrypt": vigenere_encrypt,
        "decrypt": vigenere_decrypt
    },
    "rot": {
        "encrypt": rot_encrypt,
        "decrypt": rot_decrypt
    },
    "affine": {
        "encrypt": affine_encrypt,
        "decrypt": affine_decrypt
    },
    "substitution": {
        "encrypt": substitution_encrypt,
        "decrypt": substitution_decrypt
    }
}
