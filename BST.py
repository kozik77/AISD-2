# Definicja kolorów węzłów
enum_kolory = {"RED": 0, "BLACK": 1}

class Wezel:
    def __init__(self, klucz):
        self.dane = klucz
        self.rodzic = None
        self.lewy = None
        self.prawy = None
        # Każdy nowy węzeł jest domyślnie czerwony
        self.kolor = enum_kolory["RED"]

class DrzewoCzerwonoCzarne:
    def __init__(self):
        # TNULL to liść-strażnik (czarny), który zastępuje None
        self.TNULL = Wezel(0)
        self.TNULL.kolor = enum_kolory["BLACK"]
        self.korzen = self.TNULL

    # Funkcja do rekurencyjnego przejścia drzewa w porządku preorder
    def wypisz_preorder(self, wezel, wynik):
        if wezel != self.TNULL:
            wynik.append(str(wezel.dane))
            self.wypisz_preorder(wezel.lewy, wynik)
            self.wypisz_preorder(wezel.prawy, wynik)

    # Rotacja w lewo: naprawia strukturę drzewa po wstawieniu
    def obrot_w_lewo(self, x):
        y = x.prawy
        x.prawy = y.lewy
        if y.lewy != self.TNULL:
            y.lewy.rodzic = x
        y.rodzic = x.rodzic
        if x.rodzic == None:
            self.korzen = y
        elif x == x.rodzic.lewy:
            x.rodzic.lewy = y
        else:
            x.rodzic.prawy = y
        y.lewy = x
        x.rodzic = y

    # Rotacja w prawo: naprawia strukturę drzewa po wstawieniu
    def obrot_w_prawo(self, x):
        y = x.lewy
        x.lewy = y.prawy
        if y.prawy != self.TNULL:
            y.prawy.rodzic = x
        y.rodzic = x.rodzic
        if x.rodzic == None:
            self.korzen = y
        elif x == x.rodzic.prawy:
            x.rodzic.prawy = y
        else:
            x.rodzic.lewy = y
        y.prawy = x
        x.rodzic = y

    # Kluczowa funkcja naprawiająca właściwości drzewa czerwono-czarnego
    def napraw_wstawianie(self, k):
        while k.rodzic.kolor == enum_kolory["RED"]:
            if k.rodzic == k.rodzic.rodzic.prawy:
                u = k.rodzic.rodzic.lewy # Wujek węzła
                if u.kolor == enum_kolory["RED"]:
                    # Przypadek 1: Wujek jest czerwony - zmiana kolorów
                    u.kolor = enum_kolory["BLACK"]
                    k.rodzic.kolor = enum_kolory["BLACK"]
                    k.rodzic.rodzic.kolor = enum_kolory["RED"]
                    k = k.rodzic.rodzic
                else:
                    # Przypadek 2: Wujek jest czarny, k jest lewym dzieckiem
                    if k == k.rodzic.lewy:
                        k = k.rodzic
                        self.obrot_w_prawo(k)
                    # Przypadek 3: Wujek jest czarny, k jest prawym dzieckiem
                    k.rodzic.kolor = enum_kolory["BLACK"]
                    k.rodzic.rodzic.kolor = enum_kolory["RED"]
                    self.obrot_w_lewo(k.rodzic.rodzic)
            else:
                u = k.rodzic.rodzic.prawy # Wujek węzła
                if u.kolor == enum_kolory["RED"]:
                    # Przypadek 1 (lustrzany): Zmiana kolorów
                    u.kolor = enum_kolory["BLACK"]
                    k.rodzic.kolor = enum_kolory["BLACK"]
                    k.rodzic.rodzic.kolor = enum_kolory["RED"]
                    k = k.rodzic.rodzic
                else:
                    # Przypadek 2 (lustrzany): k jest prawym dzieckiem
                    if k == k.rodzic.prawy:
                        k = k.rodzic
                        self.obrot_w_lewo(k)
                    # Przypadek 3 (lustrzany): k jest lewym dzieckiem
                    k.rodzic.kolor = enum_kolory["BLACK"]
                    k.rodzic.rodzic.kolor = enum_kolory["RED"]
                    self.obrot_w_prawo(k.rodzic.rodzic)
            if k == self.korzen:
                break
        # Korzeń musi być zawsze czarny
        self.korzen.kolor = enum_kolory["BLACK"]

    # Standardowe wstawianie do BST z późniejszym wywołaniem naprawy
    def wstaw(self, klucz):
        wezel = Wezel(klucz)
        wezel.lewy = self.TNULL
        wezel.prawy = self.TNULL
        
        y = None
        x = self.korzen

        # Znajdź miejsce dla nowego elementu
        while x != self.TNULL:
            y = x
            if wezel.dane < x.dane:
                x = x.lewy
            else:
                x = x.prawy

        wezel.rodzic = y
        if y == None:
            self.korzen = wezel
        elif wezel.dane < y.dane:
            y.lewy = wezel
        else:
            y.prawy = wezel

        # Jeśli to nie jest korzeń, napraw drzewo
        if wezel.rodzic == None:
            wezel.kolor = enum_kolory["BLACK"]
            return
        if wezel.rodzic.rodzic == None:
            return

        self.napraw_wstawianie(wezel)

# --- Przykładowe użycie ---
if __name__ == "__main__":
    dane_wejsciowe = [10, 20, 30, 15, 25, 5, 1]
    drzewo = DrzewoCzerwonoCzarne()
    
    for n in dane_wejsciowe:
        drzewo.wstaw(n)
    
    wynik_preorder = []
    drzewo.wypisz_preorder(drzewo.korzen, wynik_preorder)
    
    print("Porządek preorder w zrównoważonym drzewie BST:")
    print(" ".join(wynik_preorder))