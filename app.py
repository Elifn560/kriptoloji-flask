from flask import Flask, render_template, request, jsonify
import string
import math

app = Flask(__name__, static_folder='static', template_folder='templates')

ALPHABET = string.ascii_uppercase

# ---------- Helpers ----------
def sanitize_text(t):
    return ''.join(ch for ch in t.upper() if ch.isalpha())

def modinv(a, m):
    
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


# 1) Caesar
def caesar_encrypt(plain, shift):
    plain = plain.upper()
    res = []
    for ch in plain:
        if ch.isalpha():
            idx = ord(ch) - ord('A')
            res.append(chr((idx + shift) % 26 + ord('A')))
        else:
            res.append(ch)
    return ''.join(res)

def caesar_decrypt(cipher, shift):
    return caesar_encrypt(cipher, -shift)

# 2) Vigenere
def vigenere_encrypt(plain, key):
    plain = plain.upper()
    key = sanitize_text(key)
    if not key: return ""
    res = []
    ki = 0
    for ch in plain:
        if ch.isalpha():
            k = ord(key[ki % len(key)]) - ord('A')
            res.append(chr((ord(ch) - ord('A') + k) % 26 + ord('A')))
            ki += 1
        else:
            res.append(ch)
    return ''.join(res)

def vigenere_decrypt(cipher, key):
    cipher = cipher.upper()
    key = sanitize_text(key)
    if not key: return ""
    res = []
    ki = 0
    for ch in cipher:
        if ch.isalpha():
            k = ord(key[ki % len(key)]) - ord('A')
            res.append(chr((ord(ch) - ord('A') - k) % 26 + ord('A')))
            ki += 1
        else:
            res.append(ch)
    return ''.join(res)

# 3) Substitution (monoalphabetic)

def substitution_encrypt(plain, key):
    plain = plain.upper()
    key = key.upper()
    mapping = {chr(ord('A')+i): key[i] for i in range(26)}
    res = []
    for ch in plain:
        res.append(mapping[ch] if ch.isalpha() else ch)
    return ''.join(res)

def substitution_decrypt(cipher, key):
    cipher = cipher.upper()
    key = key.upper()
    inv = {key[i]: chr(ord('A')+i) for i in range(26)}
    res = []
    for ch in cipher:
        res.append(inv[ch] if ch.isalpha() else ch)
    return ''.join(res)

# 4) Affine: E(x) = (a*x + b) mod 26
def affine_encrypt(plain, a, b):
    plain = plain.upper()
    res = []
    for ch in plain:
        if ch.isalpha():
            x = ord(ch) - ord('A')
            res.append(chr((a*x + b) % 26 + ord('A')))
        else:
            res.append(ch)
    return ''.join(res)

def affine_decrypt(cipher, a, b):
    inv = modinv(a, 26)
    if inv is None:
        return {"error": "a has no modular inverse mod 26 (choose a coprime with 26)"}
    res = []
    for ch in cipher.upper():
        if ch.isalpha():
            y = ord(ch) - ord('A')
            res.append(chr((inv*(y - b)) % 26 + ord('A')))
        else:
            res.append(ch)
    return ''.join(res)

# 5) Playfair
def generate_playfair_table(key):
    key = sanitize_text(key)
    table = []
    used = set()
 
    def add_char(c):
        if c == 'J': c = 'I'
        if c not in used:
            used.add(c)
            table.append(c)
    for c in key:
        add_char(c)
    for c in ALPHABET:
        add_char(c)
    # return 5x5 matrix
    return [table[i*5:(i+1)*5] for i in range(5)]

def playfair_prepare_text(text, for_encrypt=True):
    text = sanitize_text(text).replace('J','I')
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = ''
        if i+1 < len(text):
            b = text[i+1]
            if a == b:
                b = 'X'
                i += 1
            else:
                i += 2
        else:
            b = 'X'
            i += 1
        pairs.append((a,b))
    return pairs

def playfair_encrypt(plain, key):
    table = generate_playfair_table(key)
    pos = {table[r][c]: (r,c) for r in range(5) for c in range(5)}
    pairs = playfair_prepare_text(plain)
    out = []
    for a,b in pairs:
        ra, ca = pos[a]
        rb, cb = pos[b]
        if ra == rb:
            out.append(table[ra][(ca+1)%5])
            out.append(table[rb][(cb+1)%5])
        elif ca == cb:
            out.append(table[(ra+1)%5][ca])
            out.append(table[(rb+1)%5][cb])
        else:
            out.append(table[ra][cb])
            out.append(table[rb][ca])
    return ''.join(out)

def playfair_decrypt(cipher, key):
    table = generate_playfair_table(key)
    pos = {table[r][c]: (r,c) for r in range(5) for c in range(5)}
    txt = sanitize_text(cipher).replace('J','I')
    pairs = [(txt[i], txt[i+1]) for i in range(0, len(txt), 2)]
    out = []
    for a,b in pairs:
        ra, ca = pos[a]
        rb, cb = pos[b]
        if ra == rb:
            out.append(table[ra][(ca-1)%5])
            out.append(table[rb][(cb-1)%5])
        elif ca == cb:
            out.append(table[(ra-1)%5][ca])
            out.append(table[(rb-1)%5][cb])
        else:
            out.append(table[ra][cb])
            out.append(table[rb][ca])
    return ''.join(out)

# 6) Route cipher (simple columnar route)

def route_encrypt(plain, cols):
    text = sanitize_text(plain)
    if cols <= 0: return ""
    rows = math.ceil(len(text)/cols)
    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    k = 0
    for r in range(rows):
        for c in range(cols):
            if k < len(text):
                matrix[r][c] = text[k]
                k += 1
            else:
                matrix[r][c] = 'X'
    # read column-wise top-down left-right
    out = []
    for c in range(cols):
        for r in range(rows):
            out.append(matrix[r][c])
    return ''.join(out)

def route_decrypt(cipher, cols):
    cipher = sanitize_text(cipher)
    if cols <= 0: return ""
    rows = math.ceil(len(cipher)/cols)
    # fill column-wise
    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    k = 0
    for c in range(cols):
        for r in range(rows):
            if k < len(cipher):
                matrix[r][c] = cipher[k]
                k += 1
    # read row-wise
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(matrix[r][c])
    return ''.join(out).rstrip('X')

# 7) Rail Fence
def railfence_encrypt(plain, rails):
    text = sanitize_text(plain)
    if rails <= 1:
        return text
    fence = ['' for _ in range(rails)]
    rail = 0
    var = 1
    for ch in text:
        fence[rail] += ch
        rail += var
        if rail == 0 or rail == rails-1:
            var = -var
    return ''.join(fence)

def railfence_decrypt(cipher, rails):
    cipher = sanitize_text(cipher)
    if rails <= 1:
        return cipher

    pattern = []
    rail = 0
    var = 1
    for i in range(len(cipher)):
        pattern.append(rail)
        rail += var
        if rail == 0 or rail == rails-1:
            var = -var

    counts = [pattern.count(r) for r in range(rails)]
    indices = []
    k = 0
    for r in range(rails):
        indices.append(cipher[k:k+counts[r]])
        k += counts[r]
    
    pos = [0]*rails
    out = []
    for p in pattern:
        out.append(indices[p][pos[p]])
        pos[p] += 1
    return ''.join(out)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    data = request.json
    method = data.get('method')
    text = data.get('text','')
    params = data.get('params', {})
    try:
        if method == 'caesar':
            shift = int(params.get('shift', 0))
            return jsonify(result=caesar_encrypt(text, shift))
        elif method == 'vigenere':
            key = params.get('key','')
            return jsonify(result=vigenere_encrypt(text, key))
        elif method == 'substitution':
            key = params.get('key','')
            if len(key) != 26:
                return jsonify(error="Substitution key must be 26 letters"), 400
            return jsonify(result=substitution_encrypt(text, key))
        elif method == 'affine':
            a = int(params.get('a',1))
            b = int(params.get('b',0))
            if modinv(a,26) is None:
                return jsonify(error="a must be coprime with 26"), 400
            return jsonify(result=affine_encrypt(text, a, b))
        elif method == 'playfair':
            key = params.get('key','')
            return jsonify(result=playfair_encrypt(text, key))
        elif method == 'route':
            cols = int(params.get('cols',3))
            return jsonify(result=route_encrypt(text, cols))
        elif method == 'railfence':
            rails = int(params.get('rails',3))
            return jsonify(result=railfence_encrypt(text, rails))
        else:
            return jsonify(error="Unknown method"), 400
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    data = request.json
    method = data.get('method')
    text = data.get('text','')
    params = data.get('params', {})
    try:
        if method == 'caesar':
            shift = int(params.get('shift', 0))
            return jsonify(result=caesar_decrypt(text, shift))
        elif method == 'vigenere':
            key = params.get('key','')
            return jsonify(result=vigenere_decrypt(text, key))
        elif method == 'substitution':
            key = params.get('key','')
            if len(key) != 26:
                return jsonify(error="Substitution key must be 26 letters"), 400
            return jsonify(result=substitution_decrypt(text, key))
        elif method == 'affine':
            a = int(params.get('a',1))
            b = int(params.get('b',0))
            dec = affine_decrypt(text, a, b)
            if isinstance(dec, dict) and dec.get('error'):
                return jsonify(error=dec['error']), 400
            return jsonify(result=dec)
        elif method == 'playfair':
            key = params.get('key','')
            return jsonify(result=playfair_decrypt(text, key))
        elif method == 'route':
            cols = int(params.get('cols',3))
            return jsonify(result=route_decrypt(text, cols))
        elif method == 'railfence':
            rails = int(params.get('rails',3))
            return jsonify(result=railfence_decrypt(text, rails))
        else:
            return jsonify(error="Unknown method"), 400
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
