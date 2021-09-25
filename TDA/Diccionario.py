class CeldaDiccionario:
    def __init__(self, etiqueta, valor):
        self.etiqueta = etiqueta
        self.valor = valor
        self.siguiente = None
        self.anterior = None


class Diccionario:
    def __init__(self):
        self._inicio = None

    def obtener(self, texto):
        temp = self._inicio

        while temp is not None:
            if temp.etiqueta == texto:
                return temp
            else:
                temp = temp.siguiente

        return None

    def insertar(self, etiqueta, valor):
        temp = self.obtener(etiqueta)
        if temp is not None:
            temp.valor = valor

        nuevo = CeldaDiccionario(etiqueta, valor)
        if self._inicio is None:
            self._inicio = nuevo
            return

        temp = self._inicio
        while temp.siguiente is not None:
            temp = temp.siguiente

        temp.siguiente = nuevo
        nuevo.anterior = temp
