from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

dane = b"0123456789ABCDEF" * 4
klucz = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
iv = get_random_bytes(16)

ecb = AES.new(klucz, AES.MODE_ECB).encrypt(dane)
cbc = AES.new(klucz, AES.MODE_CBC, iv).encrypt(dane)

def bloki(krypto):
    return [krypto[i:i+16] for i in range(0, len(krypto), 16)]

print("Dane wejsciowe:", dane)
print("Klucz:", klucz.hex())
print("IV:", iv.hex())

print("\nECB: cztery bloki kryptogramu")
for i, b in enumerate(bloki(ecb)):
    print(f"* blok {i}: {b.hex()}")
print("\nCBC: cztery bloki kryptogramu")
for i, b in enumerate(bloki(cbc)):
    print(f"* blok {i}: {b.hex()}")

# Ktore bloki sie powtarzaja (liczba blokow unikalnych z 4), set nie zawiera duplikatow
print("\nECB unikalne bloki:", len(set(bloki(ecb))), "z 4  -> wszystkie 4 identyczne" if len(set(bloki(ecb)))==1 else "")
print("CBC unikalne bloki:", len(set(bloki(cbc))), "z 4  -> kazdy inny" if len(set(bloki(cbc)))==4 else "")

# Odszyfrowanie i porownanie z wejsciem (CBC z pierwotnym IV)
ecb_dec = AES.new(klucz, AES.MODE_ECB).decrypt(ecb)
cbc_dec = AES.new(klucz, AES.MODE_CBC, iv).decrypt(cbc)
print("\nECB: odszyfrowanie == wejscie:", ecb_dec == dane)
print("CBC: odszyfrowanie == wejscie:", cbc_dec == dane)
