class RotCipher:
    def __init__(self, n=13):
        self.n = n
    
    def encrypt(self, text):
        return ''.join([chr((ord(c) + self.n) % 256) for c in text])
    
    def decrypt(self, text):
        return ''.join([chr((ord(c) - self.n) % 256) for c in text])
