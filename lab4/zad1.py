import hashlib, os, sys

def sha256_pliku(sciezka):
    return hashlib.sha256(open(sciezka, "rb").read()).hexdigest()

plik_sum = "SHA256SUMS.txt"
katalog = os.path.dirname(os.path.abspath(plik_sum)) # sciezki sa wzgledem tego katalogu

print("Status plikow:")
for linia in open(plik_sum, encoding="utf-8"):
    linia = linia.rstrip("\n")
    if not linia:
        continue
    zapisany, wzgledna = linia.split("  ", 1)
    sciezka = os.path.join(katalog, wzgledna)
    if not os.path.exists(sciezka):
        status = "BRAK"
    elif sha256_pliku(sciezka) == zapisany:
        status = "OK"
    else:
        status = "BLAD"
    print(f"{wzgledna}: {status}")

# porownanie dwoch skrotow bit po bicie
a = hashlib.sha256(b"Ala ma kota.").digest()
b = hashlib.sha256(b"Ola ma kota.").digest()
rozne_bity = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
print(f"\nRozniacych sie bitow (Ala/Ola ma kota.): {rozne_bity} z 256")