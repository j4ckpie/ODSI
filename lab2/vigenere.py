# Zadanie 2

import sys

def encrypt(data, key):
    result = bytearray()
    for i in range(len(data)):
        # dodajemy kolejny bajt klucza
        code = (data[i] + key[i % len(key)]) % 256
        result.append(code)
    return bytes(result)


def decrypt(data, key):
    result = bytearray()
    for i in range(len(data)):
        # odejmujemy bajt klucza
        code = (data[i] - key[i % len(key)]) % 256
        result.append(code)
    return bytes(result)


def hex_frag(data, rozmiar=5):
    # dzieli zapis szesnastkowy na fragmenty po "rozmiar" bajtow
    cale_hex = data.hex()
    krok = rozmiar * 2  # kazdy bajt to 2 znaki hex
    return " ".join(cale_hex[i:i + krok] for i in range(0, len(cale_hex), krok))

if len(sys.argv) < 2:
    nazwa_pliku = "tekst_pl.txt"
else:
    nazwa_pliku = sys.argv[1]

# 1.
with open(nazwa_pliku, "rb") as f:
    tekst_zrodlowy = f.read()

print("Wczytano tekst")

klucz = b"ZAMEK"
kryptogram = encrypt(tekst_zrodlowy, klucz)

with open("vigenere.bin", "wb") as f:
    f.write(kryptogram)

print("Zapisano kryptogram")

odszyfrowane = decrypt(kryptogram, klucz)

print("Zgodnosc odszyfrowania ze zrodlem:", odszyfrowane == tekst_zrodlowy)
print()

# sprawdzenie pustych danych
puste = b""
c_puste = encrypt(puste, klucz)
d_puste = decrypt(c_puste, klucz)
print("Zgodnosc pustych danych:", d_puste == puste)

# sprawdzenie granicznych danych
graniczne = bytes([0, 255])
c_graniczne = encrypt(graniczne, klucz)
d_graniczne = decrypt(c_graniczne, klucz)
print("Zgodnosc granicznych danych:", d_graniczne == graniczne)

print()

# 2.
tekst_probny = b"BRAMABRAMABRAMA"

c = encrypt(tekst_probny, b"SZYFR")
print(hex_frag(c, 5))

c = encrypt(tekst_probny, b"KOD")
print(hex_frag(c, 5))

# 3.
# Tekst 'BRAMABRAMABRAMA' ma 3 pięciobajtowe fragmenty.
# Klucz 'SZYFR' ma długość 5 (tyle co jeden "fragment" tekstu), więc każde
# powtórzenie 'BRAMA' nakłada się na ten sam fragment klucza i daje
# identyczny pięciobajtowy fragment kryptogramu.
# Klucz 'KOD' ma długość 3 (liczba inna niż długość jednego "fragmentu" tekstu).
# Kolejne powtórzenia 'BRAMA' nakładają się na przesuniętą część klucza,
# więc fragmenty kryptogramu się nie powtarzają.