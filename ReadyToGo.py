import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

class ReadyToGo(QMainWindow):
    def __init__(self):
        super().__init__()
        


app = QApplication(sys.argv)
window = ReadyToGo()
window.show()
sys.exit(app.exec_())
