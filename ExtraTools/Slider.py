from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRectF  # type: ignore
from PyQt5.QtCore import pyqtProperty  # type: ignore
from PyQt5.QtGui import QPainter, QColor


class Slider(QWidget):
    # Emits (slider_id: str, state: bool)
    toggled = pyqtSignal(str, bool)

    def __init__(self, parent=None, is_on=False, slider_id=""):
        super().__init__(parent)
        self.slider_id = slider_id
        if slider_id:
            self.setObjectName(slider_id)

        self._is_on = is_on
        self._handle_position = 1.0 if is_on else 0.0

        self.setFixedSize(60, 30)
        self.setCursor(Qt.PointingHandCursor)

        self._anim = QPropertyAnimation(self, b"handle_position", self)
        self._anim.setDuration(200)

    @pyqtProperty(float)
    def handle_position(self) -> float:
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos: float):
        self._handle_position = pos
        self.update()

    @property
    def is_on(self) -> bool:
        return self._is_on

    def set_state(self, state: bool):
        if self._is_on != state:
            self._is_on = state
            self._animate_toggle()
            # Emit BOTH id and state
            self.toggled.emit(self.slider_id, self._is_on)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_on = not self._is_on
            self._animate_toggle()
            # Emit BOTH id and state
            self.toggled.emit(self.slider_id, self._is_on)

    def _animate_toggle(self):
        self._anim.stop()
        self._anim.setStartValue(self._handle_position)
        self._anim.setEndValue(1.0 if self._is_on else 0.0)
        self._anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bg_off = QColor("#cccccc")
        bg_on = QColor("#4cd964")

        current_bg = QColor(
            int(bg_off.red() + (bg_on.red() - bg_off.red()) * self._handle_position),
            int(bg_off.green() + (bg_on.green() - bg_off.green()) * self._handle_position),
            int(bg_off.blue() + (bg_on.blue() - bg_off.blue()) * self._handle_position),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(current_bg)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)

        handle_diameter = 24
        margin = 3
        x_min = margin
        x_max = self.width() - handle_diameter - margin
        x_pos = x_min + (x_max - x_min) * self._handle_position

        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(QRectF(x_pos, margin, handle_diameter, handle_diameter))
        painter.end()