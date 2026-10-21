import math, string, sys
from collections import Counter
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def entropy(data):
    n = len(data)
    H = 0.0
    for liczba in Counter(data).values():
        p = liczba / n
        H -= p * math.log2(p)
    return H

sciezka = "slaby_ecb.bin"
krypto = open(sciezka, "rb").read()
probka = krypto[:4096] # pierwsze 4096 B

alfabet = string.ascii_lowercase + string.digits # [a-z0-9] = 36 znakow
wyniki = []
for znak in alfabet:
    klucz = (znak * 16).encode()
    plain = AES.new(klucz, AES.MODE_ECB).decrypt(probka)
    wyniki.append((znak, entropy(plain)))
wyniki.sort(key=lambda x: x[1]) # rosnaco wedlug H

print("Pieciu najlepszych kandydatow (znak, H):")
for znak, H in wyniki[:5]:
    print(f"klucz='{znak}': H={H:.4f}")

# Najlepszym kluczem odszyfruj caly plik, usun PKCS#7, sprawdz czytelnosc
znak = wyniki[0][0]
klucz = (znak * 16).encode()
tekst = unpad(AES.new(klucz, AES.MODE_ECB).decrypt(krypto), 16)
pierwszy_wiersz = tekst.split(b"\n")[0].decode("utf-8", "replace")

print(f"\nOdzyskany znak klucza: '{znak}'")
print(f"Pierwszy wiersz tekstu: {pierwszy_wiersz}")