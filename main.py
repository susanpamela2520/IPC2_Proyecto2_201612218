from GUI.GeneradorGUI import GenerarGUI
from TDA.Cola import Cola
from TDA.Pila import Pila
from XML.Lector import Lector

if __name__ == '__main__':
    # GenerarGUI()
    import os
    ROOT_DIR = os.path.abspath(os.curdir)
    print(ROOT_DIR)
    lector = Lector(ROOT_DIR + "/ArchivosDePrueba/archivo1.xml", Lector.TYPE_MAQUINA)
