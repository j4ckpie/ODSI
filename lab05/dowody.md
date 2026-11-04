# Laboratorium 5: Dowody

## Zadanie 1

### Stan przed zmianą

```
$ curl -i http://127.0.0.1:8080/materialy/
HTTP/1.1 200 OK
Content-Type: text/html;charset=ISO-8859-1

<title>Index of /materialy</title>
<h1>Index of /materialy</h1>
<li><a href="notatka.txt"> notatka.txt</a></li>
```

```
$ curl -i http://127.0.0.1:8080/materialy/notatka.txt
HTTP/1.1 200 OK
Content-Type: text/plain; charset=UTF-8

Publiczna notatka: ten plik ma pozostac dostepny pod znanym adresem.
```

```
$ curl -i http://127.0.0.1:8080/wewnetrzne/
HTTP/1.1 200 OK
Content-Type: text/html;charset=ISO-8859-1

<title>Index of /wewnetrzne</title>
<h1>Index of /wewnetrzne</h1>
<li><a href="plan.txt"> plan.txt</a></li>
```

```
$ curl -i http://127.0.0.1:8080/wewnetrzne/plan.txt
HTTP/1.1 200 OK
Content-Type: text/plain; charset=UTF-8

Fikcyjny plan: ten katalog ma byc niedostepny przez HTTP
```

### Reguły w konfiguracja/dostep.conf

```
<Directory "/usr/local/apache2/htdocs/materialy">
    Options -Indexes
    Require all granted
</Directory>
<Directory "/usr/local/apache2/htdocs/wewnetrzne">
    Require all denied
</Directory>
```

### Stan po zmianie

```
$ curl -i http://127.0.0.1:8080/materialy/
HTTP/1.1 403 Forbidden
<title>403 Forbidden</title>
```

```
$ curl -i http://127.0.0.1:8080/materialy/notatka.txt
HTTP/1.1 200 OK
Content-Type: text/plain; charset=UTF-8

Publiczna notatka: ten plik ma pozostac dostepny pod znanym adresem.
```

```
$ curl -i http://127.0.0.1:8080/wewnetrzne/
HTTP/1.1 403 Forbidden
<title>403 Forbidden</title>
```

```
$ curl -i http://127.0.0.1:8080/wewnetrzne/plan.txt
HTTP/1.1 403 Forbidden
<title>403 Forbidden</title>
```

### Wpis z logu potwierdzający odmowę

```
[Wed Nov 04 11:33:10 2026] [authz_core:error] [client 172.18.0.1] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/plan.txt
172.18.0.1 - - [04/Nov/2026:11:33:10 +0000] "GET /wewnetrzne/plan.txt HTTP/1.1" 403 239
```

## Zadanie 2

### Utworzenie konta

```
docker compose run --rm --no-deps narzedzia -cB /auth/uzytkownicy student
```

### Reguła w konfiguracja/dostep.conf

```
<Directory "/usr/local/apache2/htdocs/panel">
    AuthType Basic
    AuthName "Laboratorium 5"
    AuthUserFile "/auth/uzytkownicy"
    Require valid-user
</Directory>
```

### Testy logowania do /panel/raport.txt

```
$ curl -i http://127.0.0.1:8080/panel/raport.txt
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Laboratorium 5"
<title>401 Unauthorized</title>
```

```
$ curl -i -u student:zle http://127.0.0.1:8080/panel/raport.txt
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Laboratorium 5"
```

```
$ curl -i -u student:lab5test http://127.0.0.1:8080/panel/raport.txt
HTTP/1.1 200 OK
Content-Type: text/plain; charset=UTF-8

Raport cwiczeniowy: dostep po poprawnym uwierzytelnieniu.
```

```
$ curl -i http://127.0.0.1:8080/
HTTP/1.1 200 OK   (strona publiczna dziala bez logowania)
```

## Zadanie 3

### CGI przed Basic na cgi-bin

```
$ curl -i http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

CGI dziala
efektywny UID (euid): 2
efektywny GID (egid): 2
uzytkownik procesu: daemon
grupa procesu: daemon
/lab-data/ogolny.txt: ODCZYT OK -> LAB05: dokument dostepny dla grupy procesu WWW.
/lab-data/poufny.txt: BRAK PRAWA ODCZYTU (PermissionError)
```

### Prawa plikow w kontenerze

```
$ docker compose exec web ls -ln /lab-data/
-rw-r-----    1 0        2               48 ogolny.txt
-rw-------    1 0        2               61 poufny.txt
```

Proces CGI ma euid/egid=2 (daemon). ogolny.txt ma grupe 2 i prawo odczytu dla grupy (640)
-> CGI czyta. poufny.txt (600) ma odczyt tylko dla wlasciciela root (0) -> CGI nie czyta.

### Basic na cgi-bin

Regula dodana do konfiguracja/dostep.conf:
```
<Directory "/usr/local/apache2/cgi-bin">
    AuthType Basic
    AuthName "Laboratorium 5"
    AuthUserFile "/auth/uzytkownicy"
    Require valid-user
</Directory>
```

```
$ curl -i http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Laboratorium 5"
```

```
$ curl -i -u student:lab5test http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

CGI dziala
efektywny UID (euid): 2
efektywny GID (egid): 2
uzytkownik procesu : daemon
grupa procesu      : daemon
/lab-data/ogolny.txt: ODCZYT OK -> LAB05: dokument dostepny dla grupy procesu WWW.
/lab-data/poufny.txt: BRAK PRAWA ODCZYTU (PermissionError)
```

Po zalogowaniu euid/egid dalej = 2 (daemon) i wyniki odczytu bez zmian. Basic rozstrzyga
tylko dostep HTTP (401 vs 200), nie zmienia tozsamosci procesu ani praw do plikow.