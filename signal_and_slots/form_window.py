from PySide2 import QtWidgets as Qtw
from PySide2 import QtCore as Qtc
from PySide2 import QtGui as Qtg
import sys


class FormWindow(Qtw.QWidget):

    submitted = Qtc.Signal([str], [int, str])

    def __init__(self):
        super(FormWindow, self).__init__()
        
        self.setLayout(Qtw.QVBoxLayout())

        self.edit = Qtw.QLineEdit()
        self.submit = Qtw.QPushButton("Submit", clicked=self.onSubmit)

        self.layout().addWidget(self.edit)
        self.layout().addWidget(self.submit)

    def onSubmit(self):
        if self.edit.text().isdigit():
            text = self.edit.text()
            self.submitted[int, str].emit(int(text), text)
        else:
            self.submitted[str].emit(self.edit.text())
        self.close()



class MainWindow(Qtw.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setLayout(Qtw.QVBoxLayout())

        self.label = Qtw.QLabel("Click Change to change this text.")
        self.change = Qtw.QPushButton("Change", clicked=self.onChange)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.change)

    def onSubmittedStr(self, string):
        self.label.setText(string)
    
    def onSubmittedIntStr(self, integer, string):
        text = f"The string {string} becomes the number {integer}"
        self.label.setText(text)

    def onChange(self):
        self.form_window = FormWindow()
        self.form_window.submitted[str].connect(self.onSubmittedStr)
        self.form_window.submitted[int, str].connect(self.onSubmittedIntStr)
        self.form_window.show()  


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    calender_app = MainWindow()
    calender_app.show()
    app.exec_()