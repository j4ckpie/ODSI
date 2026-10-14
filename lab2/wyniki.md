# LAB 2

## Zadanie 1

Plik `cezar.bin` został sprawdzony dla wszystkich 256 przesunięć `k`.
Ocena (`score`) to udział bajtów drukowalnych ASCII (32-126) lub tab/CR/LF (9,10,13).

```
PS C:\Users\pietr\Desktop\STUDIA\5 semestr\ODSI\Lab2> python cezar.py cezar.bin
5 najlepszych kandydatow:
k=230, ocena=1.0, poczatek=b'Wkh#Qljkw#Ihuu|\r\rWkh'
k=233, ocena=1.0, poczatek=b'The Night Ferry\n\nThe'
k=228, ocena=0.9947534102833159, poczatek=b'Ymj%Snlmy%Kjww~\x0f\x0fYmj'
k=229, ocena=0.9947534102833159, poczatek=b'Xli$Rmklx$Jivv}\x0e\x0eXli'
k=231, ocena=0.9947534102833159, poczatek=b'Vjg"Pkijv"Hgtt{\x0c\x0cVjg'
```

### Wybrane przesuniecie: `k = 233` 
Tylko `k=233` daje tekst złożony z prawdziwych angielskich słów i znaków nowej linii (lub spacji).
Pozostali kandydaci mają wysoką ocenę tylko dlatego, że litery z alfabetu oraz znaki interpunkcyjne znajdujące się blisko ustalonego zakresu. Same znaki są "drukowalne", ale nie ukladaja się w sensowne słowa.

### Dlaczego sama entropia nie rozstrzyga
Entropia Shannona zależy wyłącznie od tego ile razy wystąpiła
dana wartość, a nie od tego, jak wartości są nazwane ani w jakiej są
kolejności. W efekcie entropia kryptogramu może być podobna dla wszystkich
256 możliwych odszyfrowań. Entropia sama w sobie nie daje żadnej
informacji, które `k` jest poprawne. Rozstrzyga dopiero sprawdzenie, czy
bajty układają się w czytelne słowa danego języka.


## Zadanie 2
```
PS C:\Users\pietr\Desktop\STUDIA\5 semestr\ODSI\Lab2> python vigenere.py tekst_pl.txt
Wczytano tekst
Zapisano kryptogram
Zgodnosc odszyfrowania ze zrodlem: True

Zgodnosc pustych danych: True
Zgodnosc granicznych danych: True

95ac9a9393 95ac9a9393 95ac9a9393    // kryptogram w hex podzielony na fragmenty po 5 bajtów
8da1859890 869d90918c 91968c9c85    // kryptogram w hex podzielony na fragmenty po 5 bajtów
```

**Wyjasnienie:**
Tekst 'BRAMABRAMABRAMA' ma 3 pięciobajtowe fragmenty.
Klucz 'SZYFR' ma długość 5 (tyle co jeden "fragment" tekstu), więc każde powtórzenie 'BRAMA' nakłada się
na ten sam fragment klucza i daje identyczny pięciobajtowy fragment kryptogramu.
Klucz 'KOD' ma długość 3 (liczba inna niż długość jednego "fragmentu" tekstu).
Kolejne powtórzenia 'BRAMA' nakładają się na przesuniętą część klucza, więc fragmenty kryptogramu się nie powtarzają.
Dla atakującego widzącego tylko kryptogram ma to znaczenie: powtarzające się bloki zdradzają, że długość klucza dzieli odległość między powtarzającymi się fragmentami w kryptogramie.

## Zadanie 3
```
PS C:\Users\pietr\Desktop\STUDIA\5 semestr\ODSI\Lab2> python rc4.py rc4.bin
Test odtworzenia RC4: True

Przeszukano 17576 kluczy w 3.030 s
5 najlepszych kandydatow (najnizsza entropia pierwszych 512 bajtow):
klucz=tat, entropia=4.3910
klucz=neg, entropia=7.4304
klucz=mcn, entropia=7.4512
klucz=oxo, entropia=7.4536
klucz=tnx, entropia=7.4592

Wybrany klucz: tat

Udzial znakow drukowalnych/bialych w odszyfrowaniu: 1.0000
Zgodnosc ponownego szyfrowania z kryptogramem: True

=== Dane do raportu ===
Wybrany klucz: 'tat'
Liczba sprawdzonych kluczy: 17576
Czas przeszukiwania: 3.030 s
Entropia calego kryptogramu: 7.9271
Entropia calego odszyfrowania: 4.3259
```

Ponowne zaszyfrowanie tym samym (choćby błędnym) kluczem zawsze “cofa” poprzednie szyfrowanie tym kluczem bo szyfrowanie i deszyfrowanie w RC4 to dokładnie ta sama operacja, więc zrobienie jej dwa razy z tym samym kluczem zawsze wraca do punktu wyjścia, niezależnie od tego, czy klucz był poprawny (XOR jest swoją odwrotnością). Ranking entropii zawiódłby przy bardzo krótkim kryptogramie (za mało danych) albo gdy prawdziwy tekst ma nietypowo wysoką entropię zbliżoną do losowego szumu.