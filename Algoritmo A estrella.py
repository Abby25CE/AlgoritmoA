import heapq

class Nodo:
    def __init__(self, estado, padre=None, costo=0, heuristica=0):
        self.estado = estado
        self.padre = padre
        self.costo = costo
        self.heuristica = heuristica
        self.total = costo + heuristica

    def __lt__(self, otro):
        return self.total < otro.total

def a_estrella(inicial, objetivo, vecinos, heuristica):
    frontera = []
    heapq.heappush(frontera, inicial)
    visitados = set()

    while frontera:
        actual = heapq.heappop(frontera)

        if actual.estado == objetivo:
            camino = []
            while actual:
                camino.append(actual.estado)
                actual = actual.padre
            return camino[::-1]

        visitados.add(actual.estado)

        for vecino, costo in vecinos(actual.estado):
            if vecino not in visitados:
                nuevo_nodo = Nodo(vecino, actual, actual.costo + costo, heuristica(vecino, objetivo))
                heapq.heappush(frontera, nuevo_nodo)

    return None

# Función para obtener los vecinos de un estado en el grafo
def vecinos_estado(estado):
    vecinos = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('D', 2)],
        'C': [('A', 4), ('D', 3)],
        'D': [('B', 2), ('C', 3), ('E', 5)],
        'E': [('D', 5)]
    }
    return vecinos.get(estado, [])

# Heurística de distancia Manhattan
def heuristica_manhattan(estado, objetivo):
    coordenadas = {
        'A': (0, 0),
        'B': (1, 0),
        'C': (0, 1),
        'D': (1, 1),
        'E': (2, 1)
    }
    x1, y1 = coordenadas[estado]
    x2, y2 = coordenadas[objetivo]
    return abs(x1 - x2) + abs(y1 - y2)

# Obtener el estado inicial y el estado objetivo del usuario
estado_inicial = input("Ingrese el estado inicial: ").upper()
estado_objetivo = input("Ingrese el estado objetivo: ").upper()

# Crear el nodo inicial y ejecutar el algoritmo A*
inicio = Nodo(estado_inicial)
camino = a_estrella(inicio, estado_objetivo, vecinos_estado, heuristica_manhattan)

if camino:
    print("Camino encontrado:", camino)
else:
    print("No se encontró un camino.")
