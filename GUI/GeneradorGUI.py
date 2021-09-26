import sys
import os
import re

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QComboBox, \
    QListWidget, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QErrorMessage, QMessageBox

# Subclass QMainWindow to customize your application's main window
from Convertidor.Convertidor import Convertidor
from TDA.Cola import Cola
from TDA.Diccionario import Diccionario
from TDA.Matriz import Matriz
from XML.Lector import Lector


class MainWindow(QMainWindow):   #Hereda de QMainWindow 
    def __init__(self):
        super().__init__()
        self._dibujar()
        self._matriz = Matriz()
        self._productos = Diccionario()

    def _dibujar(self):             #Agrego todos los botenes de la interfaz
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

        button3 = QPushButton("Iniciar")
        button3.clicked.connect(self.iniciarSimulacion)

        button4 = QPushButton("Graficar")
        button4.clicked.connect(self.graficarColaPrioridad)

        label4 = QLabel("Componentes")
        self.componentes = QListWidget()
        # self.componentes.addItems(["One", "Two", "Three"])

        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)   #No se puede editar, solo es lectura

        layout.addWidget(label, 1, 0)
        layout.addWidget(button, 1, 1)
        layout.addWidget(button2, 1, 2)
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.productos, 2, 1)
        layout.addWidget(button3, 3, 1)
        layout.addWidget(button4, 3, 2)
        layout.addWidget(label4, 4, 0)
        layout.addWidget(self.componentes, 4, 1)
        layout.addWidget(self.tableWidget, 4, 2)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
        # self.showMaximized()

        # self.setFixedSize(QSize(900, 300))

    def _mostrarError(self, mensaje):     #Mensaje de Alerta 
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error")
        dlg.setText(mensaje)
        button = dlg.exec()

    def iniciarSimulacion(self):
        text = str(self.productos.currentText())
        product = self._productos.obtener(text)
        if product is None:
            self._mostrarError("Seleccion un producto")
            return
        self._parseElaboracionAGUI(product.valor.obtener('elaboracion'))

    def graficarColaPrioridad(self):
        text = str(self.productos.currentText())   #Se obtiene producto seleccionado de combo box
        product = self._productos.obtener(text)    #Label que tiene el combo box
        if product is None:
            self._mostrarError("Seleccion un producto")
            return
        elaboracion = product.valor.obtener('elaboracion')
        paso = elaboracion.valor
        filtro_lineas = re.compile(r'L\d+p?') #uso de regex para lineas(expresion regular)
        lineas = Cola()
        lineas.llenar(filtro_lineas.findall(paso))

        filtro_componentes = re.compile(r'C\d+p?') #uso de regex para componentes
        componentes = Cola()
        componentes.llenar(filtro_componentes.findall(paso))

        paraGraficar = Cola()
        linea = lineas.obtenerInicio()
        componente = componentes.obtenerInicio()
        while linea is not None:
            paraGraficar.push(linea.valor + componente.valor)    #Union de linea y componente en una cola temporal
            linea = linea.siguiente
            componente = componente.siguiente


        paraGraficar.graficar()  

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

    def leerArchivos(self, file, file_type):   #lector XML
        lector = Lector(file, file_type)
        data = lector.leer()
        if file_type == Lector.TYPE_MAQUINA:        #si viene de maquian vamos a llenar GUI
            self.llenarGUI(data.obtener('products'))

    def llenarGUI(self, productos):         #Se utiliza el diccionario
        product = productos.valor.obtenerInicio()
        self.productos.clear()
        while product is not None:
            self.productos.addItem(product.valor.obtener('nombre').valor)    #Se llena el combo box de productos del archivo de entrada
            self._productos.insertar(product.valor.obtener('nombre').valor, product.valor)
            product = product.siguiente

    def _parseElaboracionAGUI(self, elaboracion):   #Metodo para la elaboracion de la simulacion 
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
        self._matriz = convertidor.llenarMatriz(lineas, componentes)    #se llena la matriz con el metodo llenarMatriz de Convertidor
        self._dibujarMatriz()

    def _dibujarMatriz(self):    #Llena la tabla en el grafico (tipo excel)
        filas = self._matriz.obtenerNumeroFilas()
        columnas = self._matriz.obtenerNumeroColumnas()
        self.tableWidget.setRowCount(columnas)
        self.tableWidget.setColumnCount(filas)
        # self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        for j in range(0, columnas):
            for i in range(0, filas):
                nodo = self._matriz.obtener(i, j)
                if nodo is None:
                    label = QTableWidgetItem("No hacer nada")
                else:
                    label = QTableWidgetItem(str(nodo.valor))

                self.tableWidget.setItem(j, i, label)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)


class GenerarGUI:
    def __init__(self):
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        app.exec()
