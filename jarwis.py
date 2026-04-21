import math
import random


# Otoczka wypukła - algorytm Grahama i Jarvisa
# Autor: student 2. roku informatyki



def iloczyn_wektorowy(O, A, B):
    """
    Liczy iloczyn wektorowy OA x OB.
    Jeśli wynik > 0 to skręt w lewo (CCW)
    Jeśli < 0 to skręt w prawo (CW)
    Jeśli = 0 to punkty są współliniowe
    """
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])


def odleglosc(p1, p2):
    """Zwykła odległość euklidesowa między dwoma punktami"""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)



# ALGORYTM GRAHAMA

def graham(punkty):
    """
    Algorytm Grahama - otoczka wypukła.
    
    Idea: sortujemy punkty kątowo wokół najniższego punktu,
    potem idziemy po kolei i wyrzucamy te które "skręcają w prawo"
    
    Złożoność: O(n log n) - głównie przez sortowanie
    """
    n = len(punkty)
    
    if n < 3:
        return punkty  # nie ma co liczyć
    
    # najniższy punkt - na pewno jest na otoczce
    # przy remisie biorę bardziej lewy
    pivot = min(punkty, key=lambda p: (p[1], p[0]))
    
    # sortujemy po kącie względem pivota
    def klucz(p):
        if p == pivot:
            return (-math.inf, 0)  # pivot zawsze na początku
        kat = math.atan2(p[1] - pivot[1], p[0] - pivot[0])
        dl = odleglosc(pivot, p)
        return (kat, dl)
    
    posortowane = sorted(punkty, key=klucz)
    
    # budujemy otoczkę na stosie
    stos = []
    
    for p in posortowane:
        # jeśli ostatnie trzy punkty skręcają w prawo (lub są w linii)
        # to środkowy na pewno nie jest wierzchołkiem otoczki - wyrzucamy go
        while len(stos) >= 2 and iloczyn_wektorowy(stos[-2], stos[-1], p) <= 0:
            stos.pop()
        stos.append(p)
    
    return stos



# ALGORYTM JARVISA (Gift Wrapping / Owijanie prezentu)

def jarvis(punkty):
    """
    Algorytm Jarvisa (gift wrapping - "owijanie prezentu").
    
    Idea: stoisz przy lewym skrajnym punkcie i obracasz się
    szukając kolejnego punktu otoczki - jak wskazówka zegara
    ale w drugą stronę.
    
    Złożoność: O(n * h), h = ile punktów na otoczce
    """
    n = len(punkty)
    
    if n < 3:
        return punkty  # bez sensu liczyć otoczkę z 1-2 punktów
    
    # zaczynam od najbardziej lewego punktu - na pewno jest na otoczce
    lewy = 0
    for i in range(1, n):
        if punkty[i][0] < punkty[lewy][0]:
            lewy = i
    
    otoczka = []
    obecny = lewy
    
    while True:
        otoczka.append(punkty[obecny])
        
        # kandydat na następny punkt - na razie biorę pierwszy z brzegu
        nastepny = 0
        
        for i in range(1, n):
            # iloczyn wektorowy: < 0 znaczy że i jest bardziej "w lewo"
            # niż aktualny kandydat - więc biorę i zamiast niego
            krzyz = iloczyn_wektorowy(punkty[obecny], punkty[nastepny], punkty[i])
            
            if krzyz < 0:
                nastepny = i
            elif krzyz == 0:
                # współliniowe - biorę dalszy żeby nie duplikować punktów
                if odleglosc(punkty[obecny], punkty[i]) > odleglosc(punkty[obecny], punkty[nastepny]):
                    nastepny = i
        
        obecny = nastepny
        
        # wróciłem do startu - otoczka gotowa
        if obecny == lewy:
            break
    
    return otoczka



# PORÓWNANIE WYNIKÓW

def porownaj_wyniki(punkty):
    """Uruchamia oba algorytmy i porównuje ich wyniki"""
    
    print("=" * 50)
    print("PORÓWNANIE ALGORYTMÓW OTOCZKI WYPUKŁEJ")
    print("=" * 50)
    print(f"\nLiczba punktów wejściowych: {len(punkty)}")
    print("Punkty:", punkty)
    
    # Uruchom Grahama
    print("\n--- ALGORYTM GRAHAMA ---")
    wynik_graham = graham(punkty)
    print(f"Liczba wierzchołków otoczki: {len(wynik_graham)}")
    print("Wierzchołki (CCW):", wynik_graham)
    
    # Uruchom Jarvisa
    print("\n--- ALGORYTM JARVISA ---")
    wynik_jarvis = jarvis(punkty)
    print(f"Liczba wierzchołków otoczki: {len(wynik_jarvis)}")
    print("Wierzchołki (CCW):", wynik_jarvis)
    
    # Sprawdzamy czy wyniki są równoważne
    # Normalizujemy - sortujemy żeby móc porównać
    zbior_graham = set(tuple(p) for p in wynik_graham)
    zbior_jarvis = set(tuple(p) for p in wynik_jarvis)
    
    print("\n--- PORÓWNANIE ---")
    if zbior_graham == zbior_jarvis:
        print("✓ Oba algorytmy zwróciły te same punkty otoczki!")
    else:
        print("✗ Wyniki się różnią!")
        roznica_g = zbior_graham - zbior_jarvis
        roznica_j = zbior_jarvis - zbior_graham
        if roznica_g:
            print(f"  Tylko u Grahama: {roznica_g}")
        if roznica_j:
            print(f"  Tylko u Jarvisa: {roznica_j}")
    
    return wynik_graham, wynik_jarvis



# FUNKCJA POMOCNICZA - wczytywanie od użytkownika

def wczytaj_punkty():
    """Wczytuje n i n punktów od użytkownika"""
    n = int(input("Podaj liczbę punktów n: "))
    punkty = []
    print(f"Podaj {n} punktów w formacie: x y (każdy w nowej linii)")
    print("Zakres współrzędnych: [-100, 100]")
    for i in range(n):
        while True:
            try:
                linia = input(f"Punkt {i+1}: ").split()
                x, y = int(linia[0]), int(linia[1])
                if -100 <= x <= 100 and -100 <= y <= 100:
                    punkty.append((x, y))
                    break
                else:
                    print("Błąd: współrzędne muszą być w zakresie [-100, 100]!")
            except (ValueError, IndexError):
                print("Błąd: podaj dwie liczby całkowite oddzielone spacją!")
    return punkty



# PRZYKŁADY TESTOWE

def testy():
    print("\n" + "=" * 50)
    print("TEST 1: Prosty kwadrat")
    print("=" * 50)
    punkty1 = [(0, 0), (4, 0), (4, 4), (0, 4), (2, 2)]  # środek powinien być wewnątrz
    porownaj_wyniki(punkty1)
    
    print("\n" + "=" * 50)
    print("TEST 2: Losowe punkty")
    print("=" * 50)
    random.seed(42)  # seed żeby wyniki były powtarzalne
    punkty2 = [(random.randint(-50, 50), random.randint(-50, 50)) for _ in range(10)]
    porownaj_wyniki(punkty2)
    
    print("\n" + "=" * 50)
    print("TEST 3: Punkty na okręgu (wszystkie na otoczce)")
    print("=" * 50)
    punkty3 = []
    for i in range(8):
        kat = 2 * math.pi * i / 8
        x = round(50 * math.cos(kat))
        y = round(50 * math.sin(kat))
        punkty3.append((x, y))
    porownaj_wyniki(punkty3)
    
    print("\n" + "=" * 50)
    print("TEST 4: Współliniowe punkty")
    print("=" * 50)
    punkty4 = [(0, 0), (1, 0), (2, 0), (3, 0), (1, 1), (2, 2)]
    porownaj_wyniki(punkty4)



# GŁÓWNY PROGRAM

if __name__ == "__main__":
    print("OTOCZKA WYPUKŁA - algorytmy Grahama i Jarvisa")
    print("Wybierz tryb:")
    print("1 - Wczytaj punkty ręcznie")
    print("2 - Uruchom testy automatyczne")
    
    wybor = input("Twój wybór (1/2): ").strip()
    
    if wybor == "1":
        punkty = wczytaj_punkty()
        porownaj_wyniki(punkty)
    elif wybor == "2":
        testy()
    else:
        print("Nieprawidłowy wybór, uruchamiam testy...")
        testy()