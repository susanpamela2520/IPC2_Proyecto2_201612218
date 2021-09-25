import sys
import os
import re

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QComboBox, \
    QListWidget, QFileDialog, QTableWidget

# Subclass QMainWindow to customize your application's main window
from Convertidor.Convertidor import Convertidor
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

        convertidor = Convertidor()
        self._matriz = convertidor.llenarMatriz(lineas, componentes)




class GenerarGUI:
    def __init__(self):
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        app.exec()
