from threading import Thread
from typing import Any
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QCheckBox, QComboBox, QRadioButton, QGroupBox
from PyQt5.QtCore import Qt, QTimer
from ExtraTools import ControlBox
import sys

# flag
flag = True
# CENTER_VERTICAL =
# CENTER_HORIZONTAL =

class ReadyToGo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ready To Go!")
        self.setGeometry(100, 100, 300, 300)

        self.setStyleSheet(
            "QMainWindow{border-radius: 5px; margin: 5px; background-color: #222222;}"
            "QLabel{border-radius: 5px; margin: 5px; font-size: 20px; background-color: #444444; color: white; "
            "qproperty-alignment: AlignCenter;}"
            "QLineEdit{border-radius: 5px; margin: 5px; font-size: 20px; background-color: #444444; color: white;}"
            "QGroupBox{border-radius: 5px; margin: 5px; background-color: #202020;}"
        )

        self.initUI()

        # Use QTimer for safe GUI updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # Update every 100ms
        self.show()

    def initUI(self):
        self.int_label = QLabel("Hello World!")

        central_widget = QWidget()
        self.verticalLayout = QVBoxLayout()
        central_widget.setLayout(self.verticalLayout)
        self.setCentralWidget(central_widget)

        self.verticalLayout.addWidget(self.int_label)


    def get_globals(self): ...

    def update(self): ...



app = QApplication(sys.argv)
window = ReadyToGo()
window.show()
sys.exit(app.exec_())
