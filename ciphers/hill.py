class HillCipher:
    def __init__(self, key):
        """
        key formatı: "a,b,c,d"
        örnek: "3,3,2,5"
        """
        nums = list(map(int, key.split(",")))
        if len(nums) != 4:
            raise ValueError("Hill key must be 4 integers (2x2 matrix)")

        self.key_matrix = [
            [nums[0], nums[1]],
            [nums[2], nums[3]]
        ]

        self.mod = 26
        self.inv_key = self._inverse_matrix(self.key_matrix)

    # =========================
    # ENCRYPT
    # =========================
    def encrypt(self, text):
        text = text.lower().replace(" ", "")
        if len(text) % 2 != 0:
            text += "x"  # padding

        result = ""

        for i in range(0, len(text), 2):
            pair = [
                ord(text[i]) - ord("a"),
                ord(text[i+1]) - ord("a")
            ]

            c1 = (self.key_matrix[0][0] * pair[0] + self.key_matrix[0][1] * pair[1]) % self.mod
            c2 = (self.key_matrix[1][0] * pair[0] + self.key_matrix[1][1] * pair[1]) % self.mod

            result += chr(c1 + ord("a")) + chr(c2 + ord("a"))

        return result

    # =========================
    # DECRYPT
    # =========================
    def decrypt(self, text):
        text = text.lower().replace(" ", "")
        result = ""

        for i in range(0, len(text), 2):
            pair = [
                ord(text[i]) - ord("a"),
                ord(text[i+1]) - ord("a")
            ]

            p1 = (self.inv_key[0][0] * pair[0] + self.inv_key[0][1] * pair[1]) % self.mod
            p2 = (self.inv_key[1][0] * pair[0] + self.inv_key[1][1] * pair[1]) % self.mod

            result += chr(p1 + ord("a")) + chr(p2 + ord("a"))

        return result

    # =========================
    # MATRIX INVERSE (2x2)
    # =========================
    def _inverse_matrix(self, m):
        a, b = m[0]
        c, d = m[1]

        det = (a * d - b * c) % self.mod
        det_inv = self._mod_inverse(det)

        return [
            [( d * det_inv) % self.mod, (-b * det_inv) % self.mod],
            [(-c * det_inv) % self.mod, ( a * det_inv) % self.mod]
        ]

    def _mod_inverse(self, x):
        for i in range(1, self.mod):
            if (x * i) % self.mod == 1:
                return i
        raise ValueError("Key matrix is not invertible modulo 26")
