import sys
from PySide2 import QtWidgets as Qtw
from PySide2 import QtGui as Qtg
from PySide2 import QtCore as Qtc

class MainWindow(Qtw.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.data = ["Hamburger", "CheeseBurger", "Chicken Nuggets", "Hot Dog", "Fish Sandwich"]

        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        self.listwidget = Qtw.QListWidget()
        self.combobox = Qtw.QComboBox()

        # self.add_items()

    def create_layouts(self):
        layout = Qtw.QVBoxLayout()
        layout.addWidget(self.listwidget)
        layout.addWidget(self.combobox)

        self.setLayout(layout)

    def add_items(self):
        self.listwidget.addItems(self.data)
        self.combobox.addItems(self.data)

if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec_()