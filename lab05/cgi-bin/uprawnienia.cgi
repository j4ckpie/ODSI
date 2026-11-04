#!/usr/bin/python3
import os
print("Content-Type: text/plain; charset=utf-8")
print()
print("CGI dziala")
print(f"efektywny UID (euid): {os.geteuid()}")
print(f"efektywny GID (egid): {os.getegid()}")
try:
    import pwd, grp
    print(f"uzytkownik procesu: {pwd.getpwuid(os.geteuid()).pw_name}")
    print(f"grupa procesu: {grp.getgrgid(os.getegid()).gr_name}")
except Exception:
    pass
for sciezka in ("/lab-data/ogolny.txt", "/lab-data/poufny.txt"):
    try:
        with open(sciezka, "rb") as f:
            tresc = f.read().decode("utf-8", "replace").strip()
        print(f"{sciezka}: ODCZYT OK -> {tresc}")
    except PermissionError:
        print(f"{sciezka}: BRAK PRAWA ODCZYTU (PermissionError)")
    except FileNotFoundError:
        print(f"{sciezka}: BRAK PLIKU")
