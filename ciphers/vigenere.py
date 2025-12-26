class VigenereCipher:
    def __init__(self, key='KEY'):
        self.key = key
    
    def encrypt(self, text):
        return ''.join([chr((ord(c) + ord(self.key[i % len(self.key)])) % 256) for i, c in enumerate(text)])
    
    def decrypt(self, text):
        return ''.join([chr((ord(c) - ord(self.key[i % len(self.key)])) % 256) for i, c in enumerate(text)])
