import heapq

class Node:
    def __init__(self, estado, padre=None):
        self.estado = estado
        self.padre = padre
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def heuristica(inicio, meta):
    # Calcula la distancia Manhattan entre un punto y la meta
    return abs(inicio[0] - meta[0]) + abs(inicio[1] - meta[1])

def expandir_vecinos(node, filas, columnas, laberinto):
    # Obtiene los vecinos válidos de un Node en el laberinto
    vecinos = []
    posiciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Abajo, arriba, derecha, izquierda

    for posicion in posiciones:
        fila = node.estado[0] + posicion[0]
        columna = node.estado[1] + posicion[1]
        if 0 <= fila < filas and 0 <= columna < columnas and laberinto[fila][columna] != '#':
            vecinos.append(Node((fila, columna), node))

    return vecinos

def leer_laberinto(archivo):
    # Lee el laberinto desde un archivo de texto y devuelve una lista de listas
    with open(archivo, 'r') as file:
        laberinto = [list(line.strip()) for line in file.readlines() if line.strip()]
    return laberinto

def buscar_inicio_meta(laberinto):
    # Encuentra las coordenadas del punto de inicio (I) y el punto de meta (M) en el laberinto
    filas = len(laberinto)
    columnas = len(laberinto[0])

    for i in range(filas):
        for j in range(columnas):
            if laberinto[i][j] == 'I':
                inicio = (i, j)
            elif laberinto[i][j] == 'M':
                meta = (i, j)

    return inicio, meta

def a_iniciar_busqueda(laberinto, inicio, meta):
    filas, columnas = len(laberinto), len(laberinto[0])
    open_set = []
    closed_set = set()
    inicio_node = Node(inicio)
    meta_node = Node(meta)
    heapq.heappush(open_set, inicio_node)

    while open_set:
        node_actual = heapq.heappop(open_set)

        if node_actual.estado == meta:
            camino = []
            costo_total = node_actual.g  # Costo total para llegar a la meta
            while node_actual.padre:
                camino.insert(0, node_actual.estado)
                node_actual = node_actual.padre
            camino.insert(0, inicio)
            return camino, costo_total

        closed_set.add(node_actual.estado)

        for vecino in expandir_vecinos(node_actual, filas, columnas, laberinto):
            if vecino.estado in closed_set:
                continue

            vecino.g = node_actual.g + 1  # Costo del movimiento: 1
            vecino.h = heuristica(vecino.estado, meta)
            vecino.f = vecino.g + vecino.h

            if vecino in open_set:
                node_explorado = next(n for n in open_set if n == vecino)
                if vecino.g < node_explorado.g:
                    node_explorado.g = vecino.g
                    node_explorado.padre = vecino.padre
            else:
                heapq.heappush(open_set, vecino)

    return None, None  # No se encontró un camino válido

laberinto_archivo = 'pipicucu.txt'
laberinto = leer_laberinto(laberinto_archivo)

if not laberinto:
    print("El laberinto está vacío.")
    exit()

inicio, meta = buscar_inicio_meta(laberinto)

if inicio is None or meta is None:
    print("No se encontraron el punto de inicio (I) o el punto de meta (M) en el laberinto.")
    exit()

camino, costo_total = a_iniciar_busqueda(laberinto, inicio, meta)

if camino:
    print("Camino encontrado:")
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[fila])):
            if (fila, columna) in camino:
                print('*', end=' ')
            else:
                print(laberinto[fila][columna], end=' ')
        print()
    print("Costo total:", costo_total)
else:
    print("No se encontró un camino válido.")
