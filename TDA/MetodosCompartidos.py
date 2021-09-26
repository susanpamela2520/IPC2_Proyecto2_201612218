import graphviz

class MetodosCompartidos:   #Todo referenta a la cola, como grafica, el tamaño, si esta llena o vacia
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

    def graficar(self):    #grafica para mostrar con cola.graficar
        print(self.__class__.__name__)
        dot = graphviz.Digraph(comment=self.__class__.__name__, format='png')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='box')
        temp = self._inicio
        counter = 0
        while temp is not None:
            dot.node(str(counter), str(temp.valor))
            temp = temp.siguiente
            if temp is not None:
                dot.edge(str(counter), str(counter + 1))

            counter += 1

        dot.view('./graficas/'+self.__class__.__name__)
