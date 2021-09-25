import sys
import os
import re

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QComboBox, \
    QListWidget, QFileDialog, QTableWidget

# Subclass QMainWindow to customize your application's main window
from TDA.Cola import Cola
from TDA.Matriz import Matriz
from XML.Lector import Lector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._draw()
        self._matriz = Matriz()

    def _draw(self):
        self.setWindowTitle("IPC2")

        layout = QGridLayout()

        label = QLabel("Selecciona archivos")

        button = QPushButton("Maquina")
        button.clicked.connect(self.openFileNameDialog)

        button2 = QPushButton("Simulacion")
        button2.clicked.connect(self.openFileNamesDialog)

        label3 = QLabel("Productos para simular")
        self.productos = QComboBox()
        # self.productos.addItems(["One", "Two", "Three"])

        label4 = QLabel("Componentes")
        self.componentes = QListWidget()
        # self.componentes.addItems(["One", "Two", "Three"])

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(label, 1, 0)
        layout.addWidget(button, 1, 1)
        layout.addWidget(button2, 1, 2)
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.productos, 2, 1)
        layout.addWidget(label4, 3, 0)
        layout.addWidget(self.componentes, 3, 1)
        layout.addWidget(self.tableWidget, 3, 2)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

        # self.setFixedSize(QSize(400, 300))

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "Elige un archivo", "",
                                              "XML Files (*.xml)", options=options)
        if file:
            print(file)
            self.leerArchivos(file, Lector.TYPE_MAQUINA)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Elige uno o mas archivos", "",
                                                "XML Files (*.xml)", options=options)
        if files:
            for file in files:
                self.leerArchivos(file, Lector.TYPE_SIMULACION)

    def leerArchivos(self, file, file_type):
        lector = Lector(file, file_type)
        data = lector.leer()
        # print(data)
        self.llenarGUI(data.obtener('products'))

    def llenarGUI(self, productos):
        product = productos.valor.obtenerInicio()
        while product is not None:
            self.productos.addItem(product.valor.obtener('nombre').valor)
            self._parseElaboracionAGUI(product.valor.obtener('elaboracion'))
            product = product.siguiente

    def _parseElaboracionAGUI(self, elaboracion):
        paso = elaboracion.valor
        filtro_lineas = re.compile(r'L\d+p?')
        lineas = Cola()
        lineas.llenar(filtro_lineas.findall(paso))

        filtro_componentes = re.compile(r'C\d+p?')
        componentes = Cola()
        componentes.llenar(filtro_componentes.findall(paso))

        cabeza = componentes.obtenerInicio()
        while cabeza is not None:
            self.componentes.addItem(cabeza.valor)
            cabeza = cabeza.siguiente

        self._llenarMatriz(lineas, componentes)

    def _llenarMatriz(self, lineas, componentes):
        # for item in elaboracion:
        linea = lineas.obtenerInicio()
        componente = componentes.obtenerInicio()

        while linea is not None:
            x = linea.valor.replace("L", "")
            x = int(x.replace("p", "")) - 1
            y = componente.valor.replace("C", "")
            y = int(y.replace("p", "")) - 1

            inicio = 0
            # Donde esta ahorita? como saber cual fue el ultimo componente visitado? en que lugar esta cada linea?
            for i in range(inicio, y + 1):
                #     check if move can be made. Hay ensamble en este fila?
                print("buscando ",x, i)
                temp = self._matriz.obtener(0, i)
                # temp = nodo.abajo
                esta_ensamblando = False
                while temp is not None:
                    if 'Ensamblando' in temp.valor:
                        esta_ensamblando = True
                        break
                    temp = temp.siguiente

                if esta_ensamblando is True:
                    #     si si hay ensamble dejar como no hacer nada
                    self._matriz.insertar(x, i, 'No hacer nada')
                else:
                    #     si no hay ensamble proceder al siguiente movimiento
                    self._matriz.insertar(x, i, 'Mover brazo – componente ' + str(i + 1))

            linea = linea.siguiente
            componente = componente.siguiente

            i = y
            while True:
                # verificar si se puede ensamblar
                temp = self._matriz.obtener(0, i)
                # temp = nodo.abajo
                esta_vacio = True
                while temp is not None:
                    if 'No hacer nada' != temp.valor:
                        esta_vacio = False
                        break
                    temp = temp.siguiente

                if esta_vacio and self._matriz.obtener(x, i) is None:
                    self._matriz.insertar(x, i, 'Ensamblar componente ' + str(y + 1))
                    temp = self._matriz.obtener(0, i)
                    if temp is None:
                        self._matriz.insertar(0, i, 'No hacer nada')

                    temp = self._matriz.obtener(0, i)
                    j = 0
                    while temp is not None:
                        if j != x:
                            self._matriz.insertar(j, i, 'No hacer nada')
                        j += 1
                        temp = temp.siguiente
                    break
                else:
                    self._matriz.insertar(x, i, 'No hacer nada')

                i += 1

            self._matriz.imprimir()
        print("**************************")
        self._matriz.imprimir()


class GenerarGUI:
    def __init__(self):
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        app.exec()
