import os
import sys
from PySide2 import QtWidgets as Qtw
from PySide2 import QtGui as Qtg
from PySide2 import QtCore as Qtc

class Model(Qtc.QObject):
    
    error = Qtc.Signal(str)

    def save(self, filename, content):
        print("Save Called")
        error = ""
        
        if not filename:
            error = "Filename Empty"
        elif os.path.exists(filename):
            error = f"Will not overwrite {filename}"
        else:
            try:
                with open(filename, "w") as fh:
                    fh.write(content)
            except Exception as e:
                error = f"Cannot Write file: {e}"
        
        if error:
            self.error.emit(error)


class View(Qtw.QWidget):
    submitted = Qtc.Signal(str, str)

    def __init__(self):
        super(View, self).__init__()
        self.setLayout(Qtw.QVBoxLayout())
        self.filename = Qtw.QLineEdit()
        self.filecontent = Qtw.QTextEdit()
        self.save_button = Qtw.QPushButton("Save", clicked=self.submit)

        self.layout().addWidget(self.filename)
        self.layout().addWidget(self.filecontent)
        self.layout().addWidget(self.save_button)

    def submit(self):
        filename = self.filename.text()
        filecontent = self.filecontent.toPlainText()
        self.submitted.emit(filename, filecontent)
    
    def show_error(self, error):
        Qtw.QMessageBox.critical(None, "Error", error)

class MainWindow(Qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.view = View()
        self.setCentralWidget(self.view)

        self.model = Model()
        self.view.submitted.connect(self.model.save)
        self.model.error.connect(self.view.show_error)


if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())