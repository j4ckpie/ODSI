"""Sejf sekretow i kalkulator - celowo podatna aplikacja do laboratorium 7.

Uruchamiaj wylacznie lokalnie, w kontenerze z pakietu. Dane sa fikcyjne.
"""
import re
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)
BAZA = "file:/dane/sekrety.db?mode=ro"

WZOR = re.compile(r"\s*(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)\s*")
DZIALANIA = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def oblicz(wyrazenie):
    if len(wyrazenie) > 100:
        raise ValueError("wejscie dluzsze niz 100 znakow")
    m = WZOR.fullmatch(wyrazenie)
    if not m:
        raise ValueError("niedozwolony format")
    a = float(m.group(1))
    op = m.group(2)
    b = float(m.group(3))
    if op == "/" and b == 0:
        raise ValueError("dzielenie przez zero")
    return DZIALANIA[op](a, b)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sekret")
def sekret():
    klucz = request.args.get("klucz", "")
    zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"
    wiersze, blad = [], None
    try:
        with sqlite3.connect(BAZA, uri=True) as db:
            wiersze = db.execute(zapytanie, (klucz,)).fetchall()
    except sqlite3.Error:
        app.logger.exception("Blad zapytania do sejfu sekretow")
        blad = "Wewnetrzny blad serwera"
    return render_template("sekret.html", klucz=klucz, zapytanie=zapytanie, wiersze=wiersze, blad=blad)


@app.route("/kalkulator")
def kalkulator():
    wyrazenie = request.args.get("wyrazenie")
    if wyrazenie is None:
        return render_template("kalkulator.html", wyrazenie="", wynik=None)
    try:
        wynik = oblicz(wyrazenie)
    except ValueError as exc:
        app.logger.info("Odrzucone wejscie kalkulatora: %s", exc)
        return "Nieprawidlowe dane", 400
    return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik=wynik)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
