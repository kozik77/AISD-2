import heapq
from collections import Counter

class Wezel:
    def __init__(self, znak, czestosc):
        self.znak = znak
        self.czestosc = czestosc
        self.lewy = None
        self.prawy = None

def zbuduj_drzewo(tekst):
    czestosci = Counter(tekst)
    kopiec = []
    
    for i, (znak, cz) in enumerate(czestosci.items()):
        heapq.heappush(kopiec, (cz, i, Wezel(znak, cz)))
        
    licznik = len(czestosci)
    
    while len(kopiec) > 1:
        c1, _, lewy = heapq.heappop(kopiec)
        c2, _, prawy = heapq.heappop(kopiec)
        
        nowy = Wezel(None, c1 + c2)
        nowy.lewy = lewy
        nowy.prawy = prawy
        
        heapq.heappush(kopiec, (c1 + c2, licznik, nowy))
        licznik += 1
        
    return heapq.heappop(kopiec)[2]

def generuj_kody(wezel, kod, slownik):
    if wezel is None:
        return
    if wezel.znak is not None:
        slownik[wezel.znak] = kod
        return
    generuj_kody(wezel.lewy, kod + "0", slownik)
    generuj_kody(wezel.prawy, kod + "1", slownik)

tekst = "to be or not to be"

print("Częstotliwość:")
czestosci = Counter(tekst)
for znak, ile in czestosci.most_common():
    print(f"{repr(znak)} : {ile}")
print()

korzen = zbuduj_drzewo(tekst)
kody = {}
generuj_kody(korzen, "", kody)

print("Kody Huffmana:")
for znak, _ in czestosci.most_common():
    print(f"{repr(znak)} : {kody[znak]}")
print()

skompresowany = ""
for z in tekst:
    skompresowany += kody[z]

print("Skompresowany tekst:")
print(skompresowany)
print()

bity_oryginal = len(tekst) * 8
bity_nowe = len(skompresowany)
procent = (1 - (bity_nowe / bity_oryginal)) * 100

print("Wyniki:")
print(f"Oryginal: {bity_oryginal} bitow")
print(f"Po kompresji: {bity_nowe} bitow")
print(f"Procent kompresji: {procent:.2f}%")