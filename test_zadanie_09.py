"""Testy dla zadania 9 — algorytm KMP.

Uruchamianie: pytest test_zadanie_09.py
"""

import random
import string

import pytest

from zadanie_09 import znajdz_wzorce_kmp, zbuduj_lps


# ---------- Podstawowe przypadki ----------

class TestPodstawowe:
    def test_jedno_wystapienie(self):
        assert znajdz_wzorce_kmp("abcdef", "cde") == [2]

    def test_brak_wystapien(self):
        assert znajdz_wzorce_kmp("abcdef", "xyz") == []

    def test_wzorzec_rowny_tekstowi(self):
        assert znajdz_wzorce_kmp("abc", "abc") == [0]

    def test_wiele_wystapien(self):
        assert znajdz_wzorce_kmp("abracadabra", "abra") == [0, 7]

    def test_pokrywajace_sie_wystapienia(self):
        # "aa" w "aaaa" -> indeksy 0, 1, 2 (mogą się nakładać)
        assert znajdz_wzorce_kmp("aaaa", "aa") == [0, 1, 2]

    def test_wzorzec_jednoznakowy(self):
        assert znajdz_wzorce_kmp("ababab", "a") == [0, 2, 4]


# ---------- Przypadki brzegowe ----------

class TestBrzegowe:
    def test_pusty_tekst(self):
        assert znajdz_wzorce_kmp("", "abc") == []

    def test_pusty_wzorzec(self):
        assert znajdz_wzorce_kmp("abc", "") == []

    def test_oba_puste(self):
        assert znajdz_wzorce_kmp("", "") == []

    def test_wzorzec_dluzszy_niz_tekst(self):
        assert znajdz_wzorce_kmp("ab", "abcdef") == []

    def test_wzorzec_na_koncu(self):
        assert znajdz_wzorce_kmp("hello world", "world") == [6]

    def test_wzorzec_na_poczatku(self):
        assert znajdz_wzorce_kmp("hello world", "hello") == [0]


# ---------- Polskie znaki diakrytyczne ----------

class TestPolskieZnaki:
    def test_diakrytyki(self):
        assert znajdz_wzorce_kmp("krasnoludek żółw", "żółw") == [12]

    def test_polskie_litery_powtorzenia(self):
        assert znajdz_wzorce_kmp("ąćęąćęąćę", "ąćę") == [0, 3, 6]


# ---------- Tablica LPS ----------

class TestLPS:
    def test_brak_powtorzen(self):
        assert zbuduj_lps("abcdef") == [0, 0, 0, 0, 0, 0]

    def test_klasyczny_przyklad(self):
        # "abcabd" -> [0, 0, 0, 1, 2, 0]
        assert zbuduj_lps("abcabd") == [0, 0, 0, 1, 2, 0]

    def test_same_litery(self):
        assert zbuduj_lps("aaaa") == [0, 1, 2, 3]

    def test_zlozony_przyklad(self):
        assert zbuduj_lps("ababcababc") == [0, 0, 1, 2, 0, 1, 2, 3, 4, 5]


# ---------- Testy stresowe ----------

def _naiwne_wyszukiwanie(tekst, wzorzec):
    """Brutalne wyszukiwanie O(n*m) — wyrocznia dla testów stresowych."""
    if not wzorzec or len(wzorzec) > len(tekst):
        return []
    return [
        i
        for i in range(len(tekst) - len(wzorzec) + 1)
        if tekst[i : i + len(wzorzec)] == wzorzec
    ]


@pytest.mark.parametrize("seed", range(20))
def test_stresowy_zgodnosc_z_naiwnym(seed):
    """Losujemy tekst i wzorzec, KMP musi zgadzać się z naiwnym algorytmem."""
    rnd = random.Random(seed)
    alfabet = "ab"  # mały alfabet -> wiele dopasowań i edge cases
    tekst = "".join(rnd.choices(alfabet, k=200))
    wzorzec = "".join(rnd.choices(alfabet, k=rnd.randint(1, 5)))

    assert znajdz_wzorce_kmp(tekst, wzorzec) == _naiwne_wyszukiwanie(tekst, wzorzec)


@pytest.mark.parametrize("seed", range(5))
def test_stresowy_dlugi_tekst(seed):
    """Większe rozmiary danych — sprawdzamy zgodność z naiwnym."""
    rnd = random.Random(seed)
    tekst = "".join(rnd.choices(string.ascii_lowercase, k=5000))
    wzorzec = "".join(rnd.choices(string.ascii_lowercase, k=8))

    assert znajdz_wzorce_kmp(tekst, wzorzec) == _naiwne_wyszukiwanie(tekst, wzorzec)


def test_wszystkie_pozycje_dopasowane():
    """Pesymistyczny przypadek — same identyczne znaki."""
    tekst = "a" * 1000
    wzorzec = "a" * 5
    assert znajdz_wzorce_kmp(tekst, wzorzec) == list(range(996))
