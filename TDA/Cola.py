from TDA.Celda import Celda
from TDA.MetodosCompartidos import MetodosCompartidos


class Cola(MetodosCompartidos):
    def __init__(self):
        self._inicio = None

    def push(self, valor):
        temp = self._inicio
        if temp is None:
            self._inicio = Celda(valor)
            return

        while temp.siguiente is not None:
            temp = temp.siguiente

        temp.siguiente = Celda(valor)

    def obtenerInicio(self):
        return self._inicio

    def llenar(self, desde):
        for item in desde:
            self.push(item)


