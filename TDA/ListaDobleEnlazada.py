from TDA.NodoCabecera import NodoCabecera


class ListaDobleEnlazada:
    def __init__(self):
        self._inicio = None

    def agregar(self):
        nuevo = NodoCabecera()
        temp = self._inicio

        if temp is None:
            self._inicio = nuevo
            self._inicio.x = 0
            return

        while temp.siguiente is not None:
            temp = temp.siguiente

        nuevo.x = int(temp.x) + 1
        temp.siguiente = nuevo
        nuevo.anterior = temp

    def obtener(self, index):
        tamanio = self.size()
        if tamanio <= index:
            for i in range(0, index - tamanio + 1):
                self.agregar()

        temp = self._inicio
        while temp is not None:
            if temp.x == index:
                return temp

            temp = temp.siguiente

        return None

    def recorrer(self):
        temp = self._inicio
        while temp is not None:
            print("" + str(temp.x))
            temp = temp.siguiente

    def size(self):
        contador = 0
        temp = self._inicio
        while temp is not None:
            contador += 1
            temp = temp.siguiente
        return contador

    def recorrerAlreves(self):
        temp = self._inicio
        while temp is not None:
            if temp.siguiente is None:
                break

            temp = temp.siguiente

        while temp is not None:
            print("" + str(temp.x))
            temp = temp.anterior
