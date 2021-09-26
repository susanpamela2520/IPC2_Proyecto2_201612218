from TDA.Celda import Celda
from TDA.MetodosCompartidos import MetodosCompartidos


class Pila(MetodosCompartidos):   
    def __init__(self):
        self._inicio = None

    def push(self, valor):
        if self._inicio is None:
            self._inicio = Celda(valor)
            return

        temp = Celda(valor)
        temp.siguiente = self._inicio
        self._inicio = temp

