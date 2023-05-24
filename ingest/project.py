# import Built-ins
import sys

# Import PySide2
from PySide2 import QtWidgets as Qtw
from PySide2 import QtCore as Qtc

# Import Custom Widget
from qt_os import QWidget

# Import StyleSheet
from utils import style


class Project(QWidget):
    def __init__(self, parent=None):
        super(Project, self).__init__(parent)

        # Set Window Flags
        self.setWindowFlags(Qtc.Qt.FramelessWindowHint)

        # Set Window Size
        self.resize(650, 800)
        
        # Call Widgets and Layout Methods
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        # StyleSheet
        self.setStyleSheet(style())
    
    def create_widgets(self):
        self.chooseproject_label = Qtw.QLabel()
        self.filter_line = Qtw.QLineEdit()
        self.projects_list = Qtw.QListWidget()
        self.confirm_button = Qtw.QPushButton()
        self.cancel_button = Qtw.QPushButton()

        # Set Widget Properties
        self._widget_properties()

    def _widget_properties(self):
        self.chooseproject_label.setText("Choose Project")
        self.chooseproject_label.setObjectName("choose_project")

        self.filter_line.setPlaceholderText("Filter Project...")
        self.filter_line.setObjectName("filter_project")
        
        self.confirm_button.setText("Confirm")
        self.confirm_button.setMinimumHeight(20)
        self.confirm_button.setMinimumWidth(100)

        self.cancel_button.setText("Cancel")
        self.cancel_button.setMinimumHeight(20)
        self.cancel_button.setMinimumWidth(100)

        self.projects_list.addItems(["anaconda", "bootstrap", "episodic", "feature", "commercial", "malli_pelli"])

    def create_layouts(self):
        main_layout = Qtw.QVBoxLayout()

        button_layout = Qtw.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addWidget(self.chooseproject_label)
        main_layout.addWidget(self.filter_line)
        main_layout.addWidget(self.projects_list)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def create_connections(self):
        self.cancel_button.clicked.connect(self.close)


def show():
    app = Qtw.QApplication(sys.argv)
    project_window = Project()
    project_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    show()

        