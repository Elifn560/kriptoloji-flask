# Crypto Web Client

Bu proje, klasik ve modern şifreleme algoritmalarını kullanarak
istemci–sunucu mimarisinde çalışan bir web tabanlı kriptografi uygulamasıdır.

## Kullanılan Teknolojiler
- Python (Flask)
- HTML, CSS, JavaScript
- PyCryptodome
- Wireshark (ağ trafiği analizi için)

## Desteklenen Algoritmalar

### Klasik Şifreleme Algoritmaları
- Caesar
- Vigenere
- Affine
- Rail Fence
- Playfair
- Hill
- Polybius
- ROT
- Substitution
- Pigpen

### Modern Şifreleme Algoritmaları
- AES (128-bit)
- DES
- RSA

## Uygulama Özellikleri
- Şifreleme ve çözme (Encrypt / Decrypt)
- Modern algoritmalar için anahtar girişi
- AES ve DES için manuel ve kütüphane tabanlı uygulama seçeneği
- Flask tabanlı REST endpoint (`/send`)
- Wireshark ile HTTP trafiği analizi

## Anahtar Kuralları
- **AES:** 16 byte anahtar zorunludur
- **DES:** 8 byte anahtar zorunludur
- **RSA:** Anahtarlar sunucu tarafında otomatik üretilir

## Wireshark Analizi
Uygulama çalışırken gönderilen HTTP POST istekleri Wireshark ile
yakalanmış ve simetrik şifreleme algoritmalarında anahtarın
şifrelenmeden ağ üzerinden iletildiği gözlemlenmiştir.

## Test Senaryosu
1. `python app.py` komutu ile sunucu başlatılır.
2. Tarayıcıdan `http://127.0.0.1:5000` adresine gidilir.
3. Mesaj, algoritma ve anahtar girilir.
4. Encrypt/Decrypt işlemi yapılır.
5. HTTP POST isteği Wireshark üzerinden analiz edilir.

