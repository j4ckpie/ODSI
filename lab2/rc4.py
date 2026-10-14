# Zadanie 3

import sys
import time
import math
import string
import itertools
from collections import Counter


def rc4(data, key):
    key_codes = list(key)
    key_length = len(key_codes)

    # tworzenie tablicy S
    S = list(range(256))

    # mieszanie tablicy S
    j = 0
    for i in range(256):
        j = (j + S[i] + key_codes[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    # generowanie strumienia klucza K i szyfrowanie (XOR)
    i = j = 0
    result = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(byte ^ K)
    return bytes(result)


def shannon_entropy(data):
    counts = Counter(data)
    n = len(data)
    entropy = 0.0
    for c in counts.values():
        p = c / n
        entropy -= p * math.log2(p)
    return entropy


# 1.
probny_tekst = b"Ala ma kota"
probny_klucz = b"abc"
zaszyfrowany = rc4(probny_tekst, probny_klucz)
odszyfrowany = rc4(zaszyfrowany, probny_klucz)
print("Test odtworzenia RC4:", odszyfrowany == probny_tekst)
print()

if len(sys.argv) < 2:
    nazwa_pliku = "rc4.bin"
else:
    nazwa_pliku = sys.argv[1]

# wczytanie pliku
with open(nazwa_pliku, "rb") as f:
    cryptogram = f.read()

# 2.
alfabet = string.ascii_lowercase
probka = cryptogram[:512]  # pierwsze 512 bajtow do oceny kazdego kandydata

start = time.perf_counter()

ranking = []
for litery in itertools.product(alfabet, repeat=3): # wszysktie kombinacje 3 literowe z alfabetu
    klucz = bytes(ord(c) for c in litery)
    odszyfrowana_probka = rc4(probka, klucz)
    e = shannon_entropy(odszyfrowana_probka)
    ranking.append((klucz, e))

koniec = time.perf_counter()
czas_przeszukiwania = koniec - start

# ranking rosnaco wg entropii; remisy wedlug kolejnosci alfabetycznej klucza
ranking.sort(key=lambda w: w[0])
ranking.sort(key=lambda w: w[1])

print(f"Przeszukano {len(ranking)} kluczy w {czas_przeszukiwania:.3f} s")
print("5 najlepszych kandydatow (najnizsza entropia pierwszych 512 bajtow):")
for klucz, e in ranking[:5]:
    print(f"klucz={klucz.decode('ascii')}, entropia={e:.4f}")
print()

# automatyczny wybor najlepszego kandydata
wybrany_klucz, _ = ranking[0]
print(f"Wybrany klucz: {wybrany_klucz.decode('ascii')}")
print()

# 3.
pelny_tekst = rc4(cryptogram, wybrany_klucz)

with open("rc4.txt", "wb") as f:
    f.write(pelny_tekst)

# sensownosc tekstu - udzial drukowalnych ASCII / tab / CR / LF
dozwolone = sum(1 for b in pelny_tekst if 32 <= b <= 126 or b in (9, 10, 13))
udzial = dozwolone / len(pelny_tekst) if pelny_tekst else 0.0
print(f"Udzial znakow drukowalnych/bialych w odszyfrowaniu: {udzial:.4f}")

# weryfikacja ponownego szyfrowania (nowy stan RC4) wybranym kluczem
ponowny_kryptogram = rc4(pelny_tekst, wybrany_klucz)
print("Zgodnosc ponownego szyfrowania z kryptogramem:", ponowny_kryptogram == cryptogram)
print()

# 4.
entropia_kryptogramu = shannon_entropy(cryptogram)
entropia_odszyfrowania = shannon_entropy(pelny_tekst)
print("=== Dane do raportu ===")
print(f"Wybrany klucz: {wybrany_klucz.decode('ascii')!r}")
print(f"Liczba sprawdzonych kluczy: {len(ranking)}")
print(f"Czas przeszukiwania: {czas_przeszukiwania:.3f} s")
print(f"Entropia calego kryptogramu: {entropia_kryptogramu:.4f}")
print(f"Entropia calego odszyfrowania: {entropia_odszyfrowania:.4f}")