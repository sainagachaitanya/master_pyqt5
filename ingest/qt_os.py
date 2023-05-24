# Import PySide2
from PySide2 import QtWidgets as Qtw


class QWidget(Qtw.QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

    def showEvent(self, event):
        super().showEvent(event)
        screen = Qtw.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.geometry()
        x = screen_geometry.center().x() - window_geometry.width() / 2
        y = screen_geometry.center().y() - window_geometry.height() / 2
        self.move(x, y)
