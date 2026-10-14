# Zadanie 1

import sys

def encrypt(data, key):
    result = bytearray()
    for b in data:
        # przesuniecie bajtu o klucz i zawiniecie modulo 256
        code = (b + key) % 256
        result.append(code)
    return bytes(result)


def decrypt(data, key):
    # deszyfrowanie to przesuniecie w przeciwna strone
    return encrypt(data, -key)


def score(data):
    # sprawdzamy czy bajty są drukowalne (wg instrukcji)
    dobre = 0
    for b in data:
        if 32 <= b <= 126 or b in (9, 10, 13):
            dobre += 1
    return dobre / len(data)


if len(sys.argv) < 2:
    nazwa_pliku = "cezar.bin"
else:
    nazwa_pliku = sys.argv[1]

# wczytanie pliku
with open(nazwa_pliku, "rb") as f:
    cryptogram = f.read()

# sprwadzenie wszystkich przesuniec (256)
wyniki = []
for k in range(256):
    kandydat = decrypt(cryptogram, k)
    wyniki.append((k, score(kandydat), kandydat)) # tworzymy krotke (przesuniecie, wynik, kandydat)

# remisy rosnaco wg k, potem sortowanie malejaco wg oceny
wyniki.sort(key=lambda w: w[0])
wyniki.sort(key=lambda w: w[1], reverse=True)

print("5 najlepszych kandydatow:")
for k, s, kandydat in wyniki[:5]:
    print(f"k={k}, ocena={s}, poczatek={kandydat[:20]}")
print()

# wybor reczny
k_wybrane = int(input("Podaj przesuniecie k do odszyfrowania calosci: "))
pelny_tekst = decrypt(cryptogram, k_wybrane)

# zapis wyniku
with open("cezar.txt", "wb") as f:
    f.write(pelny_tekst)