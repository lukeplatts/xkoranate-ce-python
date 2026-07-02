"""A small iOS/macOS-style toggle switch, used for the light/dark theme control.

Qt has no built-in switch widget — QCheckBox is the closest native control,
but reads as a form input rather than a live setting toggle. This paints a
pill track with a sliding knob and animates between states, which is the
vocabulary users expect for an instant, always-visible setting like theme.
"""

from PySide6.QtCore import (Property, QEasingCurve, QPropertyAnimation, QRectF,
                            Qt, Signal)
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QAbstractButton, QSizePolicy

from .. import theme


class XkorToggleSwitch(QAbstractButton):
    toggled_ = Signal(bool)  # QAbstractButton already defines `toggled`; kept for clarity

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._knobPos = 0.0  # 0 = off (light), 1 = on (dark)

        self._anim = QPropertyAnimation(self, b"knobPos", self)
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

        self.toggled.connect(self._animateTo)

    def sizeHint(self):
        return self._trackSize()

    @staticmethod
    def _trackSize():
        from PySide6.QtCore import QSize
        return QSize(40, 22)

    def _animateTo(self, checked):
        self._anim.stop()
        self._anim.setStartValue(self._knobPos)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.start()

    def getKnobPos(self):
        return self._knobPos

    def setKnobPos(self, value):
        self._knobPos = value
        self.update()

    knobPos = Property(float, getKnobPos, setKnobPos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        track = QRectF(1, 1, self.width() - 2, self.height() - 2)
        radius = track.height() / 2

        off_color = QColor(theme.muted())
        off_color.setAlphaF(0.45)
        on_color = QColor(theme.ACCENT)
        track_color = QColor(off_color)
        track_color.setRed(int(off_color.red() + (on_color.red() - off_color.red()) * self._knobPos))
        track_color.setGreen(int(off_color.green() + (on_color.green() - off_color.green()) * self._knobPos))
        track_color.setBlue(int(off_color.blue() + (on_color.blue() - off_color.blue()) * self._knobPos))

        painter.setPen(Qt.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track, radius, radius)

        knob_d = track.height() - 4
        knob_x = track.left() + 2 + (track.width() - knob_d - 4) * self._knobPos
        knob_rect = QRectF(knob_x, track.top() + 2, knob_d, knob_d)
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(knob_rect)
