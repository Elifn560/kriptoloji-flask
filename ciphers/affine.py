class AffineCipher:
    def __init__(self, a=5, b=8):
        self.a = a
        self.b = b
    
    def encrypt(self, text):
        return ''.join([chr((self.a * ord(c) + self.b) % 256) for c in text])
    
    def decrypt(self, text):
        a_inv = pow(self.a, -1, 256)
        return ''.join([chr(a_inv * (ord(c) - self.b) % 256) for c in text])
