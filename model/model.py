import copy
import random

import networkx as nx

from database.DAO import DAO
from geopy.distance import distance


class Model:
    def __init__(self):
        self._providers = DAO.getAllProviders()
        self._grafo = nx.Graph()

    def getCammino(self, target, substring):
        sources = self.getNodesMostVicini()
        source = sources[random.randint(0, len(sources) - 1)]
        if not nx.has_path(self._grafo, source, target):
            print(f"{source} e {target} non sono connessi")
            return [], source
        self._bestPath = []
        self._bestLen = 0
        parziale = [source]
        self._ricorsione(parziale, target, substring)
        return self._bestPath, source

    def _ricorsione(self, parziale, target, substring):
        if parziale[-1] == target:
            # esco ma controllo che sia soluzione ottima
            if len(parziale) > self._bestLen:
                self._bestLen = len(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return
        for v in self._grafo.neighbors(parziale[-1]):
            if v not in parziale and substring not in v.Location:
                parziale.append(v)
                self._ricorsione(parziale, target, substring)
                parziale.pop()


    def getAllProviders(self):
        return self._providers

    def buildGraph(self, provider, soglia):
        """self._nodes = DAO.getLocationOfProvider(provider)
        self._grafo.add_nodes_from(self._nodes)
        # add edges
        # modo 1: query che restituisce gli archi
        allEdges = DAO.getAllEdges(provider)
        for edge in allEdges:
            l1 = edge[0]
            l2 = edge[1]
            if l1.Location in self._nodes and l2.Location in self._nodes:
                if distance((l1.Latitude, l1.Longitude), (l2.Latitude, l2.Longitude)).km <= soglia:
                    self._grafo.add_edge(l1.Location, l2.Location, weight = distance((l1.Latitude, l1.Longitude),
                                                                   (l2.Latitude, l2.Longitude)).km)"""
        print(f"Modo 1: N nodes: {len(self._grafo.nodes)} - N edges {len(self._grafo.edges)}")
        # modo 2: modificito il metodo del DAO che legge i nodi, e ci aggiunge
        # le coordinate di una location
        # doppio ciclo sui nodi e mi calcolo le distanze in python
        self._nodes = DAO.getLocationOfProviderV2(provider)
        self._grafo.add_nodes_from(self._nodes)
        for u in self._nodes:
            for v in self._nodes:
                if u != v:
                    dist = distance((u.Latitude, u.Longitude), (v.Latitude, v.Longitude))
                    if dist <= soglia:
                        self._grafo.add_edge(u, v, weight=dist)
        print(f"Modo 2: N nodes: {len(self._grafo.nodes)} - N edges {len(self._grafo.edges)}")

        # modo 3: doppio ciclo sui nodi e per ogni "possibile" arco faccio una query (evitabile)

    def getNodesMostVicini(self):
        listTuple = []
        for u in self._nodes:
            listTuple.append((u, len(list(self._grafo.neighbors(u)))))

        listTuple.sort(key=lambda x: x[1], reverse=True)
        # result1 = filter(lambda x: x[1] == listTuple[0][1], listTuple)
        result2 = [x for x in listTuple if x[1] == listTuple[0][1]]
        return result2

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getAllLocations(self):
        return self._nodes
