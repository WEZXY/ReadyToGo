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
    def __init__(self, callerGlobals):
        super().__init__()
        self.setWindowTitle("Ready To Go!")
        self.setGeometry(100, 100, 300, 300)
        self.callerGlobals=callerGlobals
        self.controledGlobals=callerGlobals

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

    def get_globals(self):
        # Use real type objects instead of strings
        allowed_types = (
            str, int, float, complex,
            list, tuple, range, dict, set, frozenset,
            bool, bytes, bytearray, memoryview, type(None)
        )

        new_globals = {}
        for key, value in self.callerGlobals.items():
            # Check that the key doesn't start with '_' and value matches allowed types
            if not key.startswith("_") and isinstance(value, allowed_types):
                new_globals[key] = value

        self.controledGlobals = new_globals

    def update(self):
        for key in self.controledGlobals:
            self.controledGlobals[key]=None

    def open_extra_window(self):
        """Instantiate and show the interactive extra window."""
        # Create window if it doesn't exist, passing self.update_status as callback
        if self.extra_window is None:
            self.extra_window = ControlBox(self, self.update_status, "name", "var")

        self.extra_window.show()
        self.extra_window.activateWindow()  # Bring window to focus

    def update_status(self, varName, state):
        """Receives data from the extra window and updates the UI."""
        if state:
            self.display_label.show()
        else:
            self.display_label.hide()


app = QApplication(sys.argv)
window = ReadyToGo()
window.show()
sys.exit(app.exec_())
