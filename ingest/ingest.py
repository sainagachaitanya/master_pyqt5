# Import built-ins
import sys

# Import PySide2
from PySide2 import QtWidgets as Qtw
from PySide2 import QtCore as Qtc
from PySide2 import QtGui as Qtg

# import qt_os widgets
from qt_os import QWidget


class Ingest(QWidget):
    def __init__(self, parent=None):
        super(Ingest, self).__init__(parent)

        # set window title
        self.setWindowTitle("Ingest")

        # Resize Window
        self.setFixedSize(1300, 800)

        # Call Create Methods
        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        self.project_label = Qtw.QLabel()
        self.project_name = Qtw.QLabel()
        self.change_project_btn = Qtw.QPushButton()
        self.help_btn = Qtw.QPushButton()

        self._widget_properties()
        self._tab_widget()

    def _widget_properties(self):
        self.project_label.setText("MP")
        self.project_name.setText("Malli Pelli")
        self.change_project_btn.setText("Change Project")
        self.help_btn.setText("?")

    def _tab_widget(self):
        self.tab_widget = Qtw.QTabWidget()
        self.tab_widget.addTab(Qtw.QWidget(), "Create")
        self.tab_widget.addTab(Qtw.QWidget(), "Publish")
        self.tab_widget.addTab(Qtw.QWidget(), "Report")
        self.tab_widget.addTab(Qtw.QWidget(), "Details")

    def create_layouts(self):
        
        top_layout = Qtw.QHBoxLayout()
        top_layout.addWidget(self.project_label)
        top_layout.addWidget(self.project_name)
        top_layout.addStretch()
        top_layout.addWidget(self.change_project_btn)
        top_layout.addWidget(self.help_btn)


        main_layout = Qtw.QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)




def show():
    app = Qtw.QApplication(sys.argv)
    project_window = Ingest()
    project_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    show()