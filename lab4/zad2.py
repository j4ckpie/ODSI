import hashlib, hmac, os, sys

plik = "hasla.txt"

baza = {}
for linia in open(plik, encoding="utf-8"):
    linia = linia.strip()
    if not linia:
        continue
    login, iteracje, sol_hex, skrot_hex = linia.split(":")
    baza[login] = (int(iteracje), bytes.fromhex(sol_hex), bytes.fromhex(skrot_hex))

def weryfikuj(login, haslo):
    if login not in baza:
        return False
    iteracje, sol, skrot = baza[login]
    dk = hashlib.pbkdf2_hmac("sha256", haslo.encode("utf-8"), sol, iteracje, 32)
    return hmac.compare_digest(dk, skrot)

def dodaj(login, haslo, iteracje=600000):
    sol = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", haslo.encode("utf-8"), sol, iteracje, 32)
    baza[login] = (iteracje, sol, dk)
    return iteracje, sol, dk

print("Testy weryfikacji:")
print("anna, Kasztan-2026 ->", weryfikuj("anna", "Kasztan-2026"))
print("anna, kasztan-2026 ->", weryfikuj("anna", "kasztan-2026"))
print("piotr, Żółw na łące ->", weryfikuj("piotr", "Żółw na łące"))
print("kasia, Kasztan-2026 ->", weryfikuj("kasia", "Kasztan-2026"))

_, sol1, skrot1 = dodaj("test1", "to-samo-haslo")
_, sol2, skrot2 = dodaj("test2", "to-samo-haslo")
print("\nDwa konta z tym samym haslem:")
print("sole rowne:", sol1 == sol2)
print("skroty rowne:", skrot1 == skrot2)
print("weryfikacja test1:", weryfikuj("test1", "to-samo-haslo"))
print("weryfikacja test2:", weryfikuj("test2", "to-samo-haslo"))