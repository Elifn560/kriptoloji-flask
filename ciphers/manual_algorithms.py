import string


# =========================
# CAESAR
# =========================
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


# =========================
# VIGENERE
# =========================
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


# =========================
# ROT
# =========================
def rot_encrypt(text, key):
    return caesar_encrypt(text, int(key))

def rot_decrypt(text, key):
    return caesar_decrypt(text, int(key))


# =========================
# AFFINE
# =========================
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


# =========================
# SUBSTITUTION
# =========================
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


# =========================
# HILL CIPHER (2x2)
# =========================
class HillCipher:
    def __init__(self, key):
        nums = list(map(int, key.split(",")))
        if len(nums) != 4:
            raise ValueError("Hill key must be 4 integers (2x2 matrix)")

        self.key = [
            [nums[0], nums[1]],
            [nums[2], nums[3]]
        ]
        self.mod = 26
        self.inv_key = self._inverse_matrix()

    def encrypt(self, text):
        text = text.lower().replace(" ", "")
        if len(text) % 2 != 0:
            text += "x"  # padding

        result = ""
        for i in range(0, len(text), 2):
            p1 = ord(text[i]) - ord("a")
            p2 = ord(text[i+1]) - ord("a")

            c1 = (self.key[0][0] * p1 + self.key[0][1] * p2) % self.mod
            c2 = (self.key[1][0] * p1 + self.key[1][1] * p2) % self.mod

            result += chr(c1 + ord("a")) + chr(c2 + ord("a"))
        return result

    def decrypt(self, text):
        text = text.lower().replace(" ", "")
        result = ""

        for i in range(0, len(text), 2):
            c1 = ord(text[i]) - ord("a")
            c2 = ord(text[i+1]) - ord("a")

            p1 = (self.inv_key[0][0] * c1 + self.inv_key[0][1] * c2) % self.mod
            p2 = (self.inv_key[1][0] * c1 + self.inv_key[1][1] * c2) % self.mod

            result += chr(p1 + ord("a")) + chr(p2 + ord("a"))
        return result

    def _inverse_matrix(self):
        a, b = self.key[0]
        c, d = self.key[1]

        det = (a * d - b * c) % self.mod
        det_inv = pow(det, -1, self.mod)

        return [
            [( d * det_inv) % self.mod, (-b * det_inv) % self.mod],
            [(-c * det_inv) % self.mod, ( a * det_inv) % self.mod]
        ]


# =========================
# MANUAL ALGORITHMS MAP
# =========================
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
    },
    "hill": {
        "encrypt": lambda text, key: HillCipher(key).encrypt(text),
        "decrypt": lambda text, key: HillCipher(key).decrypt(text)
    }
}
