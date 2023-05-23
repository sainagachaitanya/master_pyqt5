import os
import sys
from PySide2 import QtWidgets as Qtw
from PySide2 import QtGui as Qtg
from PySide2 import QtCore as Qtc

class MainWindow(Qtw.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        form = Qtw.QWidget()
        self.setCentralWidget(form)
        form.setLayout(Qtw.QVBoxLayout())

        self.filename = Qtw.QLineEdit()
        self.filecontent = Qtw.QTextEdit()
        self.savebutton = Qtw.QPushButton("Save", clicked=self.save)
        form.layout().addWidget(self.filename)
        form.layout().addWidget(self.filecontent)
        form.layout().addWidget(self.savebutton)

    def save(self):
        filename = self.filename.text()
        error = ""
        
        if not filename:
            error = "Filename Empty"
        elif os.path.exists(filename):
            error = f"Will not overwrite {filename}"
        else:
            try:
                with open(filename, "w") as fh:
                    fh.write(self.filecontent.toPlainText())
            except Exception as e:
                error = f"Cannot write file: {e}"
            if error:
                Qtw.QMessageBox.critical(None, "Error", error)

if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())