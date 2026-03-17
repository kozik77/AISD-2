from collections import defaultdict, deque

# to samo ale z BFS 
class EdmondsKarp:
    def __init__(self, n):
        self.n = n
        self.graph = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u, v, capacity):
        # tak samo jak wyzej
        self.graph[u][v] += capacity

    def bfs(self, source, sink, parent):
        # BFS zeby znalezc najkrotsza sciezke (liczba krawedzi)
        # parent trzyma skad przyszlismy do danego wierzcholka
        odwiedzone = set([source])
        kolejka = deque([source])

        while kolejka:
            u = kolejka.popleft()
            for v, przepustowosc in self.graph[u].items():
                # idziemy tylko tam gdzie nie bylismy i jest przepustowosc
                if v not in odwiedzone and przepustowosc > 0:
                    odwiedzone.add(v)
                    parent[v] = u  # zapamietujemy skad przyszlismy
                    if v == sink:
                        return True  # dotarlismy do celu!!
                    kolejka.append(v)

        return False  

    def max_flow(self, source, sink):
        total = 0

        while True:
            parent = {}  # slownik do odtworzenia sciezki
            if not self.bfs(source, sink, parent):
                break  # nie ma juz sciezek powiekszajacych

            # odtwarzamy sciezke od sinka do source i szukamy waskiego gardla
            flow = float('inf')
            v = sink
            while v != source:
                u = parent[v]
                flow = min(flow, self.graph[u][v])
                v = u  # cofamy sie po sciezce

            # teraz aktualizujemy przepustowosci na znalezionej sciezce
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= flow   # zmniejszamy na wprost
                self.graph[v][u] += flow   # zwiekszamy powrotna
                v = u

            total += flow  # dodajemy znaleziony przeplyw do sumy

        return total


# testujemy na przykladowym grafie
ek = EdmondsKarp(6)
ek.add_edge(0, 1, 10)
ek.add_edge(0, 2, 10)
ek.add_edge(1, 3, 10)
ek.add_edge(2, 4, 10)
ek.add_edge(3, 5, 10)
ek.add_edge(4, 5, 10)
ek.add_edge(1, 2, 2)
print("Maks przeplyw:", ek.max_flow(0, 5))  # tez 20, git