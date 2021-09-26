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

    def obtenerInicio(self):  #de donde inicia (la cabeza de la cola) para hacer el llenado despues
        return self._inicio

    def llenar(self, desde):  #Combierte el array en cola para hacer el llenado
        for item in desde:
            self.push(item)


#Funcion regex lo utilizo para leer las lineas de procesamiento (Clase Generados GUI)
#regrex devuelve un array 
#el array se convierte en nodo para llenar la cola