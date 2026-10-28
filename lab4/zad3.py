import hashlib, sys

def h24(dane):
    return hashlib.sha256(dane).hexdigest()[:6]

def wariant(wiersze, v):
    out = b""
    for i, w in enumerate(wiersze):
        spacja = b" " if (v >> i) & 1 else b""
        out += w + spacja + b"\n"
    return out

def wczytaj_wiersze(sciezka):
    dane = open(sciezka, "rb").read()
    return dane.rstrip(b"\n").split(b"\n")

orig_plik = "oryginal.txt"
zmie_plik = "zmieniony.txt"
wiersze_o = wczytaj_wiersze(orig_plik)
wiersze_z = wczytaj_wiersze(zmie_plik)

# 1. slownik h24
skroty_orig = {}
for v in range(8192):
    skroty_orig.setdefault(h24(wariant(wiersze_o, v)), v)

# 2. szukamy jednej pary o rownym h24
para = None
for vz in range(8192):
    h = h24(wariant(wiersze_z, vz))
    if h in skroty_orig:
        para = (skroty_orig[h], vz, h)
        break

if para:
    print(f"Para kolizyjna: v_oryginal={para[0]}, v_zmieniony={para[1]}, h24={para[2]}")
else:
    print("Nie znaleziono pary kolizyjnej")

# 3. ile wariantow zmienionego ma h24 rowny h24 oryginalu
cel = h24(wariant(wiersze_o, 0))
ile = sum(1 for vz in range(8192) if h24(wariant(wiersze_z, vz)) == cel)
print(f"h24 oryginalu (wariant 0): {cel}")
print(f"Wariantow zmienionego o tym samym h24: {ile} z 8192")