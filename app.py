from flask import Flask, request, jsonify, render_template
from ciphers.caesar import CaesarCipher
from ciphers.vigenere import VigenereCipher
from ciphers.affine import AffineCipher
from ciphers.railfence import RailFenceCipher
from ciphers.playfair import PlayfairCipher
from ciphers.hill import HillCipher
from ciphers.polybius import PolybiusCipher
from ciphers.rot import RotCipher
from ciphers.substitution import SubstitutionCipher
from ciphers.pigpen import PigpenCipher
from manual_crypto import manual_aes_encrypt, manual_aes_decrypt, manual_des_encrypt, manual_des_decrypt
from Crypto.Cipher import AES, DES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

app = Flask(__name__)

AES_KEY = b'16byteslongkey!!'
DES_KEY = b'8bytesk'
rsa_key = RSA.generate(2048)
private_key = rsa_key
public_key = rsa_key.publickey()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    alg = data.get('algorithm')
    mode = data.get('mode', 'library')
    operation = data.get('operation')
    msg = data.get('message')

    result = "Unsupported algorithm"

    # ----------------- Klasik -----------------
    if alg == 'caesar':
        cipher = CaesarCipher()
        result = cipher.encrypt(msg) if operation=='encrypt' else cipher.decrypt(msg)
    elif alg == 'vigenere':
        cipher = VigenereCipher()
        result = cipher.encrypt(msg) if operation=='encrypt' else cipher.decrypt(msg)
    elif alg == 'affine':
        cipher = AffineCipher()
        result = cipher.encrypt(msg) if operation=='encrypt' else cipher.decrypt(msg)
    elif alg == 'railfence':
        cipher = RailFenceCipher()
        result = cipher.encrypt(msg) if operation=='encrypt' else cipher.decrypt(msg)
    elif alg == 'playfair':
        cipher = PlayfairCipher()
        result = cipher.encrypt(msg) if operation=='encrypt' else cipher.decrypt(msg)
    elif alg == 'hill':
        cipher = HillCipher()
        result = cipher.encrypt(msg) if operation=='encrypt' else cipher.decrypt(msg)
    elif alg == 'polybius':
        cipher = PolybiusCipher()
        result = cipher.encrypt(msg) if operation=='encrypt' else cipher.decrypt(msg)
    elif alg == 'rot':
        cipher = RotCipher()
        result = cipher.encrypt(msg) if operation=='encrypt' else cipher.decrypt(msg)
    elif alg == 'substitution':
        cipher = SubstitutionCipher()
        result = cipher.encrypt(msg) if operation=='encrypt' else cipher.decrypt(msg)
    elif alg == 'pigpen':
        cipher = PigpenCipher()
        result = cipher.encrypt(msg) if operation=='encrypt' else cipher.decrypt(msg)

    # ----------------- AES/DES/RSA -----------------
    elif alg.lower() == 'aes':
        if mode == 'manual':
            result = manual_aes_encrypt(msg) if operation=='encrypt' else manual_aes_decrypt(msg)
        else:
            cipher = AES.new(AES_KEY, AES.MODE_ECB)
            padded = msg.encode()
            while len(padded) % 16 != 0:
                padded += b' '
            encrypted = cipher.encrypt(padded)
            result = base64.b64encode(encrypted).decode()
    elif alg.lower() == 'des':
        if mode == 'manual':
            result = manual_des_encrypt(msg) if operation=='encrypt' else manual_des_decrypt(msg)
        else:
            cipher = DES.new(DES_KEY, DES.MODE_ECB)
            padded = msg.encode()
            while len(padded) % 8 != 0:
                padded += b' '
            encrypted = cipher.encrypt(padded)
            result = base64.b64encode(encrypted).decode()
    elif alg.lower() == 'rsa':
        if operation == 'encrypt':
            cipher = PKCS1_OAEP.new(public_key)
            encrypted = cipher.encrypt(msg.encode())
            result = base64.b64encode(encrypted).decode()
        else:
            cipher = PKCS1_OAEP.new(private_key)
            decrypted = cipher.decrypt(base64.b64decode(msg))
            result = decrypted.decode()

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
