class SubstitutionCipher:
    def __init__(self, key=None):
        self.key = key or {i: (i+5) % 256 for i in range(256)}
    
    def encrypt(self, text):
        return ''.join([chr(self.key[ord(c)]) for c in text])
    
    def decrypt(self, text):
        inv_key = {v:k for k,v in self.key.items()}
        return ''.join([chr(inv_key[ord(c)]) for c in text])
