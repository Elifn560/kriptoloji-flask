class CaesarCipher:
    def __init__(self, shift=3):
        self.shift = shift
    
    def encrypt(self, text):
        return ''.join([chr((ord(c) + self.shift) % 256) for c in text])
    
    def decrypt(self, text):
        return ''.join([chr((ord(c) - self.shift) % 256) for c in text])
