from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5 import QtGui


def set_drop_shadow(widget, blur_radius=30, x_offset=0, y_offset=10, opacity=80):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setXOffset(x_offset)
    shadow.setYOffset(y_offset)
    shadow.setColor(QtGui.QColor(0, 0, 0, opacity))
    widget.setGraphicsEffect(shadow)
