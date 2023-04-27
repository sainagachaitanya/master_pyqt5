from PySide2 import QtWidgets as Qtw
from PySide2 import QtCore as Qtc
import sys


class CategoryWindow(Qtw.QWidget):
    """A basic dialog to demonstrate inter-widget communication"""

    # when submitted, we'll emit this signal
    # with the entered string
    submitted = Qtc.Signal(str)

    def __init__(self):
        super(CategoryWindow, self).__init__()

        self.setLayout(Qtw.QVBoxLayout())
        self.layout().addWidget(
            Qtw.QLabel('Please enter a new catgory name:')
            )
        self.category_entry = Qtw.QLineEdit()
        self.layout().addWidget(self.category_entry)

        self.submit_btn = Qtw.QPushButton(
            'Submit',
            clicked=self.onSubmit
            )
        self.layout().addWidget(self.submit_btn)
        self.cancel_btn = Qtw.QPushButton(
            'Cancel',
            # Errata:  The book contains this line:
            #clicked=self.destroy
            # It should call self.close instead, like so:
            clicked=self.close
            )
        self.layout().addWidget(self.cancel_btn)
        self.show()

    @Qtc.Slot()
    def onSubmit(self):
        if self.category_entry.text():
            self.submitted.emit(self.category_entry.text())
        self.close()



class CalenderApp(Qtw.QWidget):
    events = {}

    def __init__(self):
        super(CalenderApp, self).__init__()

        self.setWindowTitle("Calender Form")
        self.resize(800, 600)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.fill_widgets()
        self.widget_properties()
        self.check_delete_btn()

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
        self.allday_check.toggled.connect(self.event_time.setDisabled)
        self.calender.selectionChanged.connect(self.populate_list)
        self.event_list.itemSelectionChanged.connect(self.populate_form)
        self.event_list.itemSelectionChanged.connect(self.check_delete_btn)
        self.add_button.clicked.connect(self.save_event)
        self.delete_button.clicked.connect(self.delete_event)
        self.event_category.currentTextChanged.connect(self.on_category_change)
        self.close_button.clicked.connect(self.close)

    def add_category(self, category):
        self.event_category.addItem(category)
        self.event_category.setCurrentText(category)
    
    def on_category_change(self, text):
        if text == "New...":
            global dialog
            dialog = CategoryWindow()
            dialog.submitted.connect(self.add_category)
            self.event_category.setCurrentIndex(0)

    def clear_form(self):
        self.event_title.clear()
        self.event_category.setCurrentIndex(0)
        self.event_time.setTime(Qtc.QTime(8, 0))
        self.allday_check.setChecked(False)
        self.event_detail.setPlainText("")

    def populate_list(self):
        self.event_list.clear()
        self.clear_form()

        date = self.calender.selectedDate()
        for event in self.events.get(date, []):
            time = (event["time"].toString("hh:mm") if event["time"] else "All Day")
            self.event_list.addItem(f"{time}: {event['title']}")

    def populate_form(self):
        self.clear_form()
        date = self.calender.selectedDate()

        event_number = self.event_list.currentRow()
        if event_number == -1:
            return
        
        event_data = self.events.get(date)[event_number]
        self.event_category.setCurrentText(event_data["category"])
        if event_data["time"] is None:
            self.allday_check.setChecked(True)
        else:
            self.event_time.setTime(event_data["time"])
        
        self.event_title.setText(event_data["title"])
        self.event_detail.setPlainText(event_data["detail"])

    def save_event(self):
        event = {
            "category": self.event_category.currentText(),
            "time": None if self.allday_check.isChecked() else self.event_time.time(),
            "title": self.event_title.text(),
            "detail": self.event_detail.toPlainText()
        }

        date = self.calender.selectedDate()
        event_list = self.events.get(date, [])
        event_number = self.event_list.currentRow()

        if event_number == -1:
            event_list.append(event)
        else:
            event_list[event_number] = event

        event_list.sort(key=lambda x: x["time"] or Qtc.QTime(0, 0))
        self.events[date] = event_list
        self.populate_list()

    def delete_event(self):
        date = self.calender.selectedDate()
        row = self.event_list.currentRow()
        del(self.events[date][row])
        self.event_list.setCurrentRow(-1)
        self.clear_form()
        self.populate_list()

    def check_delete_btn(self):
        self.delete_button.setDisabled(self.event_list.currentRow() == -1)

if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    calender_app = CalenderApp()
    calender_app.show()
    app.exec_()