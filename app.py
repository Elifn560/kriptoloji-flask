from flask import Flask, request, jsonify, render_template
from Crypto.Cipher import AES, DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

app = Flask(__name__)

rsa_key = RSA.generate(2048)
public_key = rsa_key.publickey()
private_key = rsa_key

MODERN = ["aes", "des", "rsa"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    data = request.json

    msg = data["message"]
    alg = data["algorithm"]
    op = data["operation"]
    mode = data.get("mode")
    key = data.get("key")

    if alg not in MODERN:
        key = None
        mode = None

    # AES
    if alg == "aes":
        if not key or len(key.encode()) != 16:
            return jsonify(result="AES key must be 16 bytes")

        cipher = AES.new(key.encode(), AES.MODE_ECB)

        if op == "encrypt":
            m = msg.encode()
            while len(m) % 16 != 0: m += b" "
            return jsonify(result=base64.b64encode(cipher.encrypt(m)).decode())
        else:
            return jsonify(result=cipher.decrypt(base64.b64decode(msg)).decode())

    # DES
    if alg == "des":
        if not key or len(key.encode()) != 8:
            return jsonify(result="DES key must be 8 bytes")

        cipher = DES.new(key.encode(), DES.MODE_ECB)

        if op == "encrypt":
            m = msg.encode()
            while len(m) % 8 != 0: m += b" "
            return jsonify(result=base64.b64encode(cipher.encrypt(m)).decode())
        else:
            return jsonify(result=cipher.decrypt(base64.b64decode(msg)).decode())

    # RSA
    if alg == "rsa":
        if op == "encrypt":
            cipher = PKCS1_OAEP.new(public_key)
            return jsonify(result=base64.b64encode(cipher.encrypt(msg.encode())).decode())
        else:
            cipher = PKCS1_OAEP.new(private_key)
            return jsonify(result=cipher.decrypt(base64.b64decode(msg)).decode())

    return jsonify(result="OK")

if __name__ == "__main__":
    app.run(debug=True)
