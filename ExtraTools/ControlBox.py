import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QGridLayout, QLabel, QLineEdit, QPushButton
)
from Slider import Slider


class ControlBox(QWidget):
    """Secondary window with full interactive controls."""

    def __init__(self, parent_callback, *argu):
        super().__init__()
        self.parent_callback = parent_callback  # Function reference to send data back
        self.setWindowTitle("Settings & Tools - Extra Window")
        self.setGeometry(200, 200, 350, 200)
        self.setObjectName("ControlBox")

        self.setStyleSheet(
            "QWidget#ControlBox{border-radius: 5px; margin: 5px; background-color: #222222;}"
            "QLabel{border-radius: 5px; margin: 5px; font-size: 20px; background-color: #444444; color: white; "
            "qproperty-alignment: AlignCenter;}"
            "QLineEdit{border-radius: 5px; margin: 5px; font-size: 20px; background-color: #444444; color: white;}"
            "QGroupBox{border-radius: 5px; margin: 5px; background-color: #202020;}"
        )

        self.controlGlobals = argu
        # self.labelsAndSliders = {}

        self.initUI()

    def initUI(self):
        # Main layout for this window
        layout = QGridLayout()

        # 1. Add a Label
        for i in range(len(self.controlGlobals)):
            label = QLabel(self.controlGlobals[i])
            slider = Slider(slider_id=self.controlGlobals[i])
            slider.toggled.connect(self.submit_data)
            layout.addWidget(label, i, 0)
            layout.addWidget(slider, i, 1)

        self.close_btn = QPushButton("Close Window")
        self.close_btn.clicked.connect(self.close)

        layout.addWidget(self.close_btn, len(self.controlGlobals), 0, 1, 2)

        self.setLayout(layout)

    def submit_data(self, slider_id, state):
        """Handle button click inside the extra window."""
        self.parent_callback(slider_id, state)


class MainWindow(QMainWindow):
    """Main Application Window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Dashboard")
        self.setGeometry(100, 100, 400, 250)

        self.setStyleSheet(
            "QMainWindow{border-radius: 5px; margin: 5px; background-color: #222222;}"
            "QLabel{border-radius: 5px; margin: 5px; font-size: 20px; background-color: #444444; color: white; "
            "qproperty-alignment: AlignCenter;}"
            "QLineEdit{border-radius: 5px; margin: 5px; font-size: 20px; background-color: #444444; color: white;}"
            "QGroupBox{border-radius: 5px; margin: 5px; background-color: #202020;}"
        )

        # Central widget layout
        container = QWidget()
        layout = QVBoxLayout()

        # Display label on main window
        self.display_label = QLabel("Current Status: Default")
        layout.addWidget(self.display_label)

        # Button to launch secondary window
        self.open_window_btn = QPushButton("Open Controls Window")
        self.open_window_btn.clicked.connect(self.open_extra_window)
        layout.addWidget(self.open_window_btn)

        container.setLayout(layout)
        self.setCentralWidget(container)

        self.extra_window = None

    def open_extra_window(self):
        """Instantiate and show the interactive extra window."""
        # Create window if it doesn't exist, passing self.update_status as callback
        if self.extra_window is None:
            self.extra_window = ControlBox(self.update_status, "name", "var")

        self.extra_window.show()
        self.extra_window.activateWindow()  # Bring window to focus

    def update_status(self, new_text, state):
        """Receives data from the extra window and updates the UI."""
        self.display_label.setText(f"Current Status: {new_text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())