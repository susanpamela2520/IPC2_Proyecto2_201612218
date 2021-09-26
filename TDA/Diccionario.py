class CeldaDiccionario:
    def __init__(self, etiqueta, valor):
        self.etiqueta = etiqueta
        self.valor = valor
        self.siguiente = None
        self.anterior = None


class Diccionario:
    def __init__(self):
        self._inicio = None

    def obtener(self, texto):    #Recorre toda la lista
        temp = self._inicio

        while temp is not None:             #No existe retorna none
            if temp.etiqueta == texto:
                return temp
            else:
                temp = temp.siguiente

        return None

    def insertar(self, etiqueta, valor):   #Inserta valores en los espacios del diccionario 
        temp = self.obtener(etiqueta)
        if temp is not None:
            temp.valor = valor             #Verifica el valor del espacio 

        nuevo = CeldaDiccionario(etiqueta, valor)         #crea una nueva celda y la asigna al final
        if self._inicio is None:
            self._inicio = nuevo
            return

        temp = self._inicio
        while temp.siguiente is not None:
            temp = temp.siguiente

        temp.siguiente = nuevo
        nuevo.anterior = temp


#Difencia de cola y diccionario 
#la cola no verifica y el diccionario si, se necesita verificacion por las etiquetas