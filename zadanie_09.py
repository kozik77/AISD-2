"""Zadanie 9 — wyszukiwanie wzorca w tekście algorytmem KMP.

Dane:   tekst i wzorzec
Wynik:  miejsca wystąpień wzorca w tekście (lista indeksów 0-based)

Algorytm Knutha-Morrisa-Pratta (KMP):
    1. Preprocessing: tablica LPS (Longest Proper Prefix which is also Suffix)
       dla wzorca. Złożoność O(m).
    2. Skanowanie tekstu z wykorzystaniem LPS — przy niedopasowaniu cofamy się
       tylko w wzorcu (nigdy w tekście). Złożoność O(n).

Złożoność łączna:
    - czasowa: O(n + m) (zarówno średnia jak i pesymistyczna)
    - pamięciowa: O(m)

gdzie n = len(tekst), m = len(wzorzec).
"""


def zbuduj_lps(wzorzec):
    """Buduje tablicę prefix-function (LPS) dla wzorca.

    lps[i] = długość najdłuższego właściwego prefiksu wzorzec[0..i],
             który jest jednocześnie sufiksem wzorzec[0..i].

    Przykład: dla "abcabd" zwraca [0, 0, 0, 1, 2, 0].
    """
    m = len(wzorzec)
    lps = [0] * m
    dlugosc = 0  # długość ostatnio dopasowanego prefix-suffix
    i = 1

    while i < m:
        if wzorzec[i] == wzorzec[dlugosc]:
            dlugosc += 1
            lps[i] = dlugosc
            i += 1
        else:
            if dlugosc != 0:
                # Cofamy się do krótszego dopasowania, ale NIE inkrementujemy i
                dlugosc = lps[dlugosc - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def znajdz_wzorce_kmp(tekst, wzorzec):
    """Zwraca posortowaną listę indeksów początków wystąpień wzorca w tekście.

    Konwencja: pusty wzorzec zwraca pustą listę.
    """
    n = len(tekst)
    m = len(wzorzec)

    if m == 0 or m > n:
        return []

    lps = zbuduj_lps(wzorzec)

    wystapienia = []
    i = 0  # indeks w tekście
    j = 0  # indeks we wzorcu

    while i < n:
        if tekst[i] == wzorzec[j]:
            i += 1
            j += 1
            if j == m:
                # Pełne dopasowanie — zapisujemy pozycję początku
                wystapienia.append(i - m)
                # Przygotowujemy się na kolejne wystąpienie używając LPS
                j = lps[j - 1]
        else:
            if j != 0:
                # Niedopasowanie — cofamy się w wzorcu, ale NIE w tekście
                j = lps[j - 1]
            else:
                # Już na początku wzorca — przesuwamy się w tekście
                i += 1

    return wystapienia


# --- Przykładowe użycie ---
if __name__ == "__main__":
    przyklady = [
        ("abracadabra", "abra"),
        ("aaaaa", "aa"),
        ("abcdef", "xyz"),
        ("krasnoludek krasnoludek krasnoludek", "lud"),
        ("ababcababcabc", "ababc"),
    ]

    print("Wyniki wyszukiwania wzorca algorytmem KMP:\n")
    for tekst, wzorzec in przyklady:
        wynik = znajdz_wzorce_kmp(tekst, wzorzec)
        print(f"  tekst='{tekst}'")
        print(f"  wzorzec='{wzorzec}'")
        print(f"  wystapienia: {wynik}\n")

    print("Przykładowe tablice LPS:")
    for w in ["abcabd", "ababcababc", "aaaa", "abcdef"]:
        print(f"  wzorzec='{w}' lps={zbuduj_lps(w)}")
