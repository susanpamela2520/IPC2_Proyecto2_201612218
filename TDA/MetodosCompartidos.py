class MetodosCompartidos:
    def estaVacia(self):
        return self._inicio is None

    def size(self):
        contador = 0
        temp = self._inicio
        while temp is not None:
            contador += 1
            temp = temp.siguiente

        return contador

    def pop(self):
        if self._inicio is None:
            return None

        temp = self._inicio
        self._inicio = self._inicio.siguiente
        return temp.valor