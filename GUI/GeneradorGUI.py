import sys
import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QComboBox, \
    QListWidget, QFileDialog


# Subclass QMainWindow to customize your application's main window
from XML.Lector import Lector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

        layout.addWidget(label, 1, 0)
        layout.addWidget(button, 1, 1)
        layout.addWidget(button2, 1, 2)
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.productos, 2, 1)
        layout.addWidget(label4, 3, 0)
        layout.addWidget(self.componentes, 3, 1)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

        # self.setFixedSize(QSize(400, 300))

    def the_button_was_clicked(self):
        print("Clicked!")

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
            print(files)
            for file in files:
                self.leerArchivos(file, Lector.TYPE_SIMULACION)

    def leerArchivos(self, file, file_type):
        lector = Lector(file, file_type)

class GenerarGUI:
    def __init__(self):
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        app.exec()

