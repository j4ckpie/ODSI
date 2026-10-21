from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

haslo = "haslo-testowe".encode("utf-8")

def szyfruj(dane, haslo):
    sol = get_random_bytes(16)
    iv = get_random_bytes(16)
    klucz = PBKDF2(haslo, sol, dkLen=32, count=200000, hmac_hash_module=SHA256)
    krypto = AES.new(klucz, AES.MODE_CBC, iv).encrypt(pad(dane, 16))
    return sol, iv, krypto

def odszyfruj(sol, iv, krypto, haslo):
    klucz = PBKDF2(haslo, sol, dkLen=32, count=200000, hmac_hash_module=SHA256)
    return unpad(AES.new(klucz, AES.MODE_CBC, iv).decrypt(krypto), 16)

testy = [
    ("puste dane", b""),
    ("16 B ASCII", b"0123456789ABCDEF"),
    ("wiadomosc.txt", open("wiadomosc.txt", "rb").read()),
]


print("Haslo testowe:", haslo.decode())
print("\nTesty:")
for nazwa, dane in testy:
    sol, iv, krypto = szyfruj(dane, haslo)
    odtworzone = odszyfruj(sol, iv, krypto, haslo)
    print(f"{nazwa} | rowne={odtworzone == dane}, len_wejscia={len(dane)}B, len_kryptogramu={len(krypto)}B")

# to samo haslo, nowa sol i IV ---> inny kryptogram
wiadomosc = open("wiadomosc.txt", "rb").read()
_, _, krypto_a = szyfruj(wiadomosc, haslo)
_, _, krypto_b = szyfruj(wiadomosc, haslo)
print("\nDwukrotne szyfrowanie wiadomosci tym samym haslem (nowa sol i IV)")
print("kryptogramy identyczne:", krypto_a == krypto_b)