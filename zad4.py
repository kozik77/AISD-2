from collections import defaultdict

#  Fordem-Fulkersonem
class FordFulkerson:
    def __init__(self, n):
        # n to liczba wierzcholkow w grafie
        self.n = n
        self.graph = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u, v, capacity):
        # dodajemy krawedz z u do v z przepustowoscia capacity
        # krawedz powrotna ma 0 bo tak trzeba (dowiedzialem sie na wykladzie)
        self.graph[u][v] += capacity

    def dfs(self, source, sink, visited, flow):
        # jak jestesmy w sinku to zwracamy flow i git
        if source == sink:
            return flow
        visited.add(source)
        for sasiad, przepustowosc in self.graph[source].items():
            # idziemy dalej tylko jesli nie odwiedzony i jest miejsce
            if sasiad not in visited and przepustowosc > 0:
                waskie_gardlo = self.dfs(sasiad, sink, visited, min(flow, przepustowosc))
                if waskie_gardlo > 0:
                    # aktualizujemy siec resztkowa (to wazne!! bez tego nie dziala)
                    self.graph[source][sasiad] -= waskie_gardlo
                    self.graph[sasiad][source] += waskie_gardlo
                    return waskie_gardlo
        return 0  # nie ma drogi, smuteczek

    def max_flow(self, source, sink):
        total = 0
        while True:
            visited = set()
            # szukamy sciezki powiekszajacej przez DFS
            flow = self.dfs(source, sink, visited, float('inf'))
            if flow == 0:
                break  # nie ma juz sciezek, konczymy petle
            total += flow
        return total


# testujemy na przykladowym grafie
ff = FordFulkerson(6)
ff.add_edge(0, 1, 10)
ff.add_edge(0, 2, 10)
ff.add_edge(1, 3, 10)
ff.add_edge(2, 4, 10)
ff.add_edge(3, 5, 10)
ff.add_edge(4, 5, 10)
ff.add_edge(1, 2, 2)
print("Maks przeplyw:", ff.max_flow(0, 5))  # powinno byc 20