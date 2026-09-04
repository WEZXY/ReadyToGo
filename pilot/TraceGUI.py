import sys
import time
from threading import Thread
from typing import Any
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QTabWidget, QCheckBox, QComboBox,
    QRadioButton, QGroupBox, QButtonGroup, QSpinBox, QSlider
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer

flag = True
GREEN = "\033[92m"
RESET = "\033[0m"
speed = 120
# label.setText(f'Speed: <span style="color: red;">{speed}</span> km/h')

class MainWindow(QMainWindow):
    def __init__(self, *args, caller_globals=None, tracked_dict=None, controled_dict=None, slider=None, **kwargs):
        super().__init__()
        self.setWindowTitle('Trace GUI')
        self.setCentralWidget(QWidget())
        self.hbox1 = QHBoxLayout(self.centralWidget())
        self.vbox1 = QGridLayout(self.centralWidget())
        self.vbox2 = QGridLayout(self.centralWidget())
        self.group_box1 = QGroupBox(self)
        self.group_box2 = QGroupBox(self)

        # Use the caller's global namespace and tracked dictionary
        self.glbl = caller_globals or {}
        self.tracked_dict = tracked_dict or kwargs
        self.controled_dict = controled_dict or {}
        self.slider = slider or {}
        self.labels = {}
        self.line_edits = {}
        self.buttons = {}
        self.slide_bars = {}

        self.setStyleSheet(
            "QMainWindow{border-radius: 5px; margin: 5px; background-color: black;}"
            "QLabel{border-radius: 5px; margin: 5px; font-size: 20px; background-color: #444444; color: white;}"
            "QLineEdit{border-radius: 5px; margin: 5px; font-size: 20px; background-color: #444444; color: white;}"
            "QGroupBox{border-radius: 5px; margin: 5px; background-color: #202020;}"
        )

        self.initUI()
        self.trace(*args, **kwargs)
        # Use QTimer for safe GUI updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # Update every 1000ms
        self.show()

    def initUI(self):
        self.group_box1.setLayout(self.vbox1)
        self.group_box2.setLayout(self.vbox2)
        self.hbox1.addWidget(self.group_box1)
        self.hbox1.addWidget(self.group_box2)

        for i, key in enumerate(self.tracked_dict):
            value = self.glbl.get(key, self.tracked_dict[key])
            label = QLabel(f"{key}: <span style='color: green;'>{value}</span>", self)
            self.labels[key] = label
            self.vbox1.addWidget(label, i%5, i//5)

        for i, key in enumerate(self.controled_dict):
            value = self.glbl.get(key, self.controled_dict[key])
            label = QLabel(f"{key}: {value}", self)

            line_edit = QLineEdit(self)
            line_edit.setPlaceholderText("Enter value")
            line_edit.returnPressed.connect(lambda k=key: self.on_button_click(k))

            button = QPushButton("Change", self)
            button.clicked.connect(lambda _, k=key: self.on_button_click(k))

            self.labels[key] = label
            self.line_edits[key] = line_edit
            self.buttons[key] = button

            self.vbox2.addWidget(label, i, 0)
            self.vbox2.addWidget(line_edit, i, 1)
            self.vbox2.addWidget(button, i, 2)

        for i, key in enumerate(self.slider):
            i += len(self.controled_dict)
            value = int(self.glbl.get(key, self.slider[key])[0])
            print(self.glbl.get(key, self.slider[key])[1])
            v_range = list(map(int, self.glbl.get(key, self.slider[key])[1]))

            steps = 1
            if len(self.slider[key]) > 2:
                steps = self.glbl.get(key, self.slider[key])[2]
                print(v_range, steps)
                v_range[0] = int(v_range[0]/steps)
                v_range[1] = int(v_range[1]/steps)
            print(value, v_range, steps, sep="\n")
            label = QLabel(f"{key}: {value}", self)

            slide_bar = QSlider(Qt.Horizontal, self) #type: ignore
            slide_bar.setRange(*v_range)
            slide_bar.setValue(value)
            slide_bar.valueChanged.connect(lambda _, k=key, s=steps: self.on_slider_change(_, k, s))

            self.labels[key] = label
            self.slide_bars[key] = slide_bar

            self.vbox2.addWidget(label, i, 0)
            self.vbox2.addWidget(slide_bar, i, 1, 1, 2)

    def update(self):
        for key, label in self.labels.items():
            # Check glbl first, fall back to tracked_dict
            if key in self.tracked_dict: value = self.glbl.get(key, self.tracked_dict[key])
            elif key in self.controled_dict: value = self.glbl.get(key, self.controled_dict[key])
            elif key in self.slider: value = self.glbl.get(key, self.slider[key])[0]
            try: label.setText(f"{key}: <span style='color: green;'>{value:.2f}</span>")
            except: label.setText(f"{key}: <span style='color: green;'>{value}</span>")

    def trace(self, *args, **kwargs):
        # Update tracked_dict with initial kwargs if not provided
        for k, v in kwargs.items():
            if k not in self.tracked_dict:
                self.tracked_dict[k] = v

    def on_button_click(self, key, *args):
        var_type=type(self.glbl[key])
        try:
            value = var_type(self.line_edits[key].text())
            self.glbl[key] = value
        except:
            pass
        self.line_edits[key].clear()

    def on_line_edit_return(self, key):
        var_type=type(self.glbl[key])
        try:
            value = var_type(self.line_edits[key].text())
            self.glbl[key] = value
        except:
            pass
        self.line_edits[key].clear()

    def on_slider_change(self, _, key, steps=1):
        value = self.slide_bars[key].value()
        value = value*steps
        self.glbl[key][0] = value

    def closeEvent(self, event):
        global flag
        flag = False
        self.timer.stop()  # Stop the timer when closing
        event.accept()

def __run_gui(*args, caller_globals=None, tracked_dict=None, controled_dict=None, slider=None, **kwargs):
    global window1
    app = QApplication(sys.argv)
    window1 = MainWindow(*args, caller_globals=caller_globals, tracked_dict=tracked_dict, controled_dict=controled_dict
                         , slider=slider, **kwargs)
    app.exec_()  # Run the event loop without sys.exit

def create_gui(*args, caller_globals=None, tracked_dict=None, controled_dict=None, slider=None, **kwargs):
    # Start the GUI in a separate daemon thread
    Thread(target=__run_gui, args=args, kwargs={"caller_globals": caller_globals, "tracked_dict": tracked_dict
                                              , "controled_dict": controled_dict, "slider": slider, **kwargs}, daemon=True).start()
    # Return immediately to allow the importing script to continue
    return
