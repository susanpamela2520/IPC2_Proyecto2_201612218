from GUI.GeneradorGUI import GenerarGUI
from TDA.Cola import Cola
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


if __name__ == '__main__':
    GenerarGUI()


