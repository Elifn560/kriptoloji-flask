class RailFenceCipher:
    def __init__(self, rails=3):
        self.rails = rails
    
    def encrypt(self, text):
        rail = ['' for _ in range(self.rails)]
        index, step = 0, 1
        for c in text:
            rail[index] += c
            if index == 0:
                step = 1
            elif index == self.rails - 1:
                step = -1
            index += step
        return ''.join(rail)
    
    def decrypt(self, text):
        return text  # Basitleştirilmiş; tam çözüm eklenebilir
