from flask import Flask, request, jsonify, render_template
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

# klasik manuel algoritmalar
from ciphers.manual_algorithms import MANUAL_ALGORITHMS

# AES / DES (kütüphaneli)
from lib_crypto import (
    lib_aes_encrypt,
    lib_aes_decrypt,
    lib_des_encrypt,
    lib_des_decrypt
)

# AES / DES (kütüphanesiz – educational)
from manual_crypto import (
    manual_aes_encrypt,
    manual_aes_decrypt,
    manual_des_encrypt,
    manual_des_decrypt
)

app = Flask(__name__)

# ======================
# RSA anahtarları
# ======================
rsa_key = RSA.generate(2048)
public_key = rsa_key.publickey()
private_key = rsa_key


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    data = request.get_json(force=True)

    msg  = data["message"]
    alg  = data["algorithm"]
    op   = data["operation"]
    key  = data.get("key", "")
    mode = data.get("mode", "library")

    # ======================
    # MANUEL (KLASİK) ŞİFRELER
    # ======================
    if alg in MANUAL_ALGORITHMS:
        if key.strip() == "":
            return jsonify({"error": f"{alg.upper()} requires a key"})

        func = MANUAL_ALGORITHMS[alg][op]
        return jsonify({"result": func(msg, key)})

    # ======================
    # AES
    # ======================
    if alg == "aes":
        if len(key.encode()) != 16:
            return jsonify({"error": "AES key must be 16 bytes"})

        if mode == "manual":
            result = (
                manual_aes_encrypt(msg, key)
                if op == "encrypt"
                else manual_aes_decrypt(msg, key)
            )
        else:
            result = (
                lib_aes_encrypt(msg, key)
                if op == "encrypt"
                else lib_aes_decrypt(msg, key)
            )

        return jsonify({"result": result})

    # ======================
    # DES
    # ======================
    if alg == "des":
        if len(key.encode()) != 8:
            return jsonify({"error": "DES key must be 8 bytes"})

        if mode == "manual":
            result = (
                manual_des_encrypt(msg, key)
                if op == "encrypt"
                else manual_des_decrypt(msg, key)
            )
        else:
            result = (
                lib_des_encrypt(msg, key)
                if op == "encrypt"
                else lib_des_decrypt(msg, key)
            )

        return jsonify({"result": result})

    # ======================
    # RSA
    # ======================
    if alg == "rsa":
        if op == "encrypt":
            cipher = PKCS1_OAEP.new(public_key)
            return jsonify({
                "result": base64.b64encode(cipher.encrypt(msg.encode())).decode()
            })
        else:
            cipher = PKCS1_OAEP.new(private_key)
            return jsonify({
                "result": cipher.decrypt(base64.b64decode(msg)).decode()
            })

    return jsonify({"error": "Unknown algorithm"})


if __name__ == "__main__":
    app.run(debug=True)
