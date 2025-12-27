from flask import Flask, request, jsonify, render_template
from Crypto.Cipher import AES, DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

from ciphers.manual_algorithms import MANUAL_ALGORITHMS

app = Flask(__name__)

# RSA anahtarları
rsa_key = RSA.generate(2048)
public_key = rsa_key.publickey()
private_key = rsa_key


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    data = request.get_json(force=True)

    msg = data["message"]
    alg = data["algorithm"]
    op  = data["operation"]
    key = data.get("key", "")

    # =====================
    # MANUEL ALGORİTMALAR
    # =====================
    if alg in MANUAL_ALGORITHMS:
        if key.strip() == "":
            return jsonify({"error": f"{alg.upper()} requires a key"})

        func = MANUAL_ALGORITHMS[alg][op]
        return jsonify({"result": func(msg, key)})

    # =====================
    # AES
    # =====================
    if alg == "aes":
        if len(key.encode()) != 16:
            return jsonify({"error": "AES key must be 16 bytes"})

        cipher = AES.new(key.encode(), AES.MODE_ECB)

        if op == "encrypt":
            m = msg.encode()
            while len(m) % 16 != 0:
                m += b" "
            return jsonify({"result": base64.b64encode(cipher.encrypt(m)).decode()})
        else:
            return jsonify({"result": cipher.decrypt(base64.b64decode(msg)).decode().strip()})

    # =====================
    # DES
    # =====================
    if alg == "des":
        if len(key.encode()) != 8:
            return jsonify({"error": "DES key must be 8 bytes"})

        cipher = DES.new(key.encode(), DES.MODE_ECB)

        if op == "encrypt":
            m = msg.encode()
            while len(m) % 8 != 0:
                m += b" "
            return jsonify({"result": base64.b64encode(cipher.encrypt(m)).decode()})
        else:
            return jsonify({"result": cipher.decrypt(base64.b64decode(msg)).decode().strip()})

    # =====================
    # RSA
    # =====================
    if alg == "rsa":
        if op == "encrypt":
            cipher = PKCS1_OAEP.new(public_key)
            return jsonify({"result": base64.b64encode(cipher.encrypt(msg.encode())).decode()})
        else:
            cipher = PKCS1_OAEP.new(private_key)
            return jsonify({"result": cipher.decrypt(base64.b64decode(msg)).decode()})

    return jsonify({"error": "Unknown algorithm"})


if __name__ == "__main__":
    app.run(debug=True)
