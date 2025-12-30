import requests

# ==========================
# KULLANICI GİRİŞİ
# ==========================

msg = input("Enter message: ")
alg = input("Choose algorithm (caesar/vigenere/aes/des/rsa): ").lower()
op  = input("Choose operation (encrypt/decrypt): ").lower()

key = ""
mode = "library"

# AES / DES için ek seçimler
if alg in ["aes", "des"]:
    mode = input("Choose mode (library/manual): ").lower()
    key = input("Enter key: ")

# Manuel klasik algoritmalar
elif alg in ["caesar", "vigenere", "affine", "rot", "substitution"]:
    key = input("Enter key: ")

# RSA için key yok
elif alg == "rsa":
    pass

else:
    print("Unsupported algorithm")
    exit()


# ==========================
# SUNUCUYA GÖNDER
# ==========================

payload = {
    "message": msg,
    "algorithm": alg,
    "operation": op,
    "mode": mode,
    "key": key
}

response = requests.post(
    "http://127.0.0.1:5000/send",
    json=payload
)

print("\n--- SERVER RESPONSE ---")
print(response.json())
