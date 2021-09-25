from TDA.Celda import Celda
from TDA.ListaDobleEnlazada import ListaDobleEnlazada


class Matriz:
    def __init__(self):
        self._filas = ListaDobleEnlazada()
        self._columnas = ListaDobleEnlazada()

    def insertar(self, x, y, valor):
        nodo = Celda(valor, x, y)
        self._insertarFila(x, nodo)
        self._insertColumna(y, nodo)

    def _insertarFila(self, x, nodo):
        cabecera = self._filas.obtener(x)
        inicio = cabecera.abajo
        if inicio is None:
            cabecera.abajo = nodo
            nodo.arriba = inicio
        else:
            while inicio.abajo is not None:
                inicio = inicio.abajo
            inicio.abajo = nodo
            nodo.arriba = inicio

    def _insertColumna(self, y, nodo):
        cabecera = self._columnas.obtener(y)
        inicio = cabecera.abajo
        if inicio is None:
            cabecera.abajo = nodo
            nodo.arriba = inicio
        else:
            while inicio.abajo is not None:
                inicio = inicio.abajo
            inicio.abajo = nodo
            nodo.arriba = inicio

    def _obtener(self, x, y):
        cabecera = self._filas.obtener(x)
        if cabecera is None:
            return None

        inicio = cabecera.abajo
        if inicio is None:
            return None

        while inicio is not None:
            if inicio.x is x and inicio.y is y:
                return inicio
            inicio = inicio.abajo

        return None

    def imprimir(self):
        i = self._filas.size()
        j = self._columnas.size()
        for k in range(0, j):
            fila = ""
            for l in range(0, i):
                nodo = self._obtener(l, k)
                if nodo is None:
                    fila += " 0 "
                else:
                    fila += " " + str(nodo.valor) + " "
            print(fila)
