import sys
from PySide2 import QtWidgets as Qtw
from PySide2 import QtGui as Qtg
from PySide2 import QtCore as Qtc

class MainWindow(Qtw.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Fight Fighter Game Lobby")

        cx_form = Qtw.QWidget()
        cx_form.setLayout(Qtw.QFormLayout())
        self.setCentralWidget(cx_form)

        heading = Qtw.QLabel("Fight Fighter")
        heading_font = Qtg.QFont("Arial", 32, Qtg.QFont.Bold)
        heading_font.setStretch(Qtg.QFont.ExtraExpanded)
        heading.setFont(heading_font)
        cx_form.layout().addRow(heading)

        inputs = {
            "Server": Qtw.QLineEdit(),
            "Name": Qtw.QLineEdit(),
            "Password": Qtw.QLineEdit(echoMode=Qtw.QLineEdit.Password),
            "Team": Qtw.QComboBox(),
            "Ready": Qtw.QCheckBox("Check When Ready")
        }

        teams = ("Crismson Sharks", "Shadow Hawks", "Night Terrors", "Blue Crew")
        inputs["Team"].addItems(teams)

        for label, widget in inputs.items():
            cx_form.layout().addRow(label, widget)

        self.submit = Qtw.QPushButton("Connect", clicked=lambda: Qtw.QMessageBox.information(None, "Connecting", "Prepare for Battle!"))
        self.reset = Qtw.QPushButton("Cancel", clicked=self.close)
        cx_form.layout().addRow(self.submit, self.reset)


        label_font = Qtg.QFont()
        label_font.setFamily("Arial")
        label_font.setPointSize(14)
        label_font.setWeight(Qtg.QFont.DemiBold)
        label_font.setStyle(Qtg.QFont.StyleItalic)
        label_font.setStyleHint(Qtg.QFont.Fantasy)
        # label_font.setStyleStrategy(Qtg.QFont.PreferAntialias | Qtg.QFont.PreferQuality)

        for inp in inputs.values():
            cx_form.layout().labelForField(inp).setFont(label_font)

        self.submit.setFont(label_font)
        self.reset.setFont(label_font)

        go_pixmap = Qtg.QPixmap(Qtc.QSize(32, 32))
        stop_pixmap = Qtg.QPixmap(Qtc.QSize(32, 32))
        go_pixmap.fill(Qtg.QColor("green"))
        stop_pixmap.fill(Qtg.QColor("red"))

        connect_icon = Qtg.QIcon()
        connect_icon.addPixmap(go_pixmap, Qtg.QIcon.Active)
        connect_icon.addPixmap(stop_pixmap, Qtg.QIcon.Disabled)

        self.submit.setIcon(connect_icon)
        self.submit.setDisabled(True)

        inputs["Server"].textChanged.connect(lambda x: self.submit.setDisabled(x==""))

if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())