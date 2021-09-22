import sys


class GenerarGUI:
    def __init__(self):
        from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
        app = QApplication(sys.argv)
        w = QWidget()
        w.resize(500, 500)
        w.layout = QVBoxLayout()
        w.label = QLabel("Hello World!")
        w.label.setStyleSheet("font-size:25px;margin-left:155px;")
        w.setWindowTitle("PyQt5 Window")
        w.layout.addWidget(w.label)
        w.setLayout(w.layout)
        w.show()
        sys.exit(app.exec_())
