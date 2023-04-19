from PySide2 import QtWidgets as Qtw
from PySide2 import QtCore as Qtc
import sys


class CalenderApp(Qtw.QWidget):
    def __init__(self):
        super(CalenderApp, self).__init__()

        self.setWindowTitle("Calender Form")
        self.resize(800, 600)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.fill_widgets()
        self.widget_properties()

    def create_widgets(self):
        self.calender = Qtw.QCalendarWidget()
        self.event_list = Qtw.QListWidget()
        self.event_title = Qtw.QLineEdit()
        self.event_category = Qtw.QComboBox()
        self.event_time = Qtw.QTimeEdit(Qtc.QTime(8, 0))
        self.allday_check = Qtw.QCheckBox("All Day")
        self.event_detail = Qtw.QTextEdit()
        self.add_button = Qtw.QPushButton("Add/Update")
        self.delete_button = Qtw.QPushButton("Delete")
        self.close_button = Qtw.QPushButton("Close")

    def widget_properties(self):
        self.calender.setSizePolicy(Qtw.QSizePolicy.Expanding, Qtw.QSizePolicy.Expanding)
        self.event_list.setSizePolicy(Qtw.QSizePolicy.Expanding, Qtw.QSizePolicy.Expanding)

    def fill_widgets(self):
        # Add event Categories
        self.event_category.addItems( ["Select Category...", "New...", "Work", "Meeting", "Doctor", "Family"] )
        # Disable the first categpry item
        self.event_category.model().item(0).setEnabled(False)
    
    def create_layout(self):
        event_form = Qtw.QGroupBox("Event")
        event_form_layout = Qtw.QGridLayout()
        event_form_layout.addWidget(self.event_title, 1, 1, 1, 3)
        event_form_layout.addWidget(self.event_category, 2, 1)
        event_form_layout.addWidget(self.event_time, 2, 2)
        event_form_layout.addWidget(self.allday_check, 2, 3)
        event_form_layout.addWidget(self.event_detail, 3, 1, 1, 3)
        event_form_layout.addWidget(self.add_button, 4, 1)
        event_form_layout.addWidget(self.delete_button, 4, 2)
        event_form_layout.addWidget(self.close_button, 4, 3)
        event_form.setLayout(event_form_layout)

        right_layout = Qtw.QVBoxLayout()
        right_layout.addWidget(Qtw.QLabel("Events on Date"))
        right_layout.addWidget(self.event_list)
        right_layout.addWidget(event_form)
        

        main_layout = Qtw.QHBoxLayout()
        main_layout.addWidget(self.calender)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def create_connections(self):
        self.close_button.clicked.connect(self.close)


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    calender_app = CalenderApp()
    calender_app.show()
    app.exec_()