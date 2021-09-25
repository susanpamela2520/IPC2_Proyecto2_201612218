from GUI.GeneradorGUI import GenerarGUI
from TDA.Cola import Cola
from TDA.ListaDobleEnlazada import ListaDobleEnlazada
from TDA.Matriz import Matriz
from TDA.Pila import Pila
from XML.Lector import Lector

def testCola():
    cola = Cola()
    print(cola.estaVacia())
    cola.push(1)
    cola.push(2)
    print(cola.estaVacia())
    cola.push(3)
    print(cola.size())
    cola.graficar()

def testLeerXML():
    import os
    ROOT_DIR = os.path.abspath(os.curdir)
    print(ROOT_DIR)
    lector = Lector(ROOT_DIR + "/ArchivosDePrueba/archivo1.xml", Lector.TYPE_MAQUINA)

def testLindaDoble():
    fila = ListaDobleEnlazada()
    fila.agregar("a")
    fila.agregar("b")
    fila.agregar("c")
    fila.agregar("d")
    fila.recorrerAlreves()

def testMatrix():
    matriz = Matriz()
    matriz.insertar(3, 2, "a")
    matriz.insertar(3, 3, "b")
    matriz.insertar(4, 4, "d")
    matriz.insertar(0, 1, "c")
    matriz.imprimir()

if __name__ == '__main__':
    GenerarGUI()

