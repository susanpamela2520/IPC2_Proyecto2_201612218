class Celda:
    def __init__(self, valor, x = 0, y = 0):
        self.valor = valor
        self.arriba = None
        self.abajo = None
        self.siguiente = None
        self.anterior = None
        self.x = x
        self.y = y