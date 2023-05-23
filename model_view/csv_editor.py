import sys
import csv
from PySide2 import QtWidgets as Qtw
from PySide2 import QtGui as Qtg
from PySide2 import QtCore as Qtc

class CSVTableModel(Qtc.QAbstractTableModel):

    def __init__(self, csv_file):
        super(CSVTableModel, self).__init__()
        
        self.filename = csv_file

        with open(self.filename) as fh:
            csvreader = csv.reader(fh)
            self._headers = next(csvreader)
            self._data = list(csvreader)
        

if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    mw = CSVTableModel()
    mw.show()
    sys.exit(app.exec_())