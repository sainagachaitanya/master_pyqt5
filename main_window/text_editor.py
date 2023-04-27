import sys
from PySide2 import QtWidgets as Qtw
from PySide2 import QtGui as Qtg
from PySide2 import QtCore as Qtc

class MainWindow(Qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        
        settings = Qtc.QSettings("SaiChaitanya", "text_editor")
        
        # splash_screen = Qtw.QMessageBox()
        # splash_screen.setWindowTitle("My Text Editor")
        # splash_screen.setText("BETA SOFTWARE WARNING!")
        # splash_screen.setInformativeText("This is very very beta, Are you sure you want to use it?")
        # splash_screen.setDetailedText("This editor was written for learning purposes, and probably is not fit for real work")
        # splash_screen.setWindowModality(Qtc.Qt.WindowModal)
        # splash_screen.addButton(Qtw.QMessageBox.Yes)
        # splash_screen.addButton(Qtw.QMessageBox.Abort)
        # response = splash_screen.exec_()
        # if response == Qtw.QMessageBox.Abort:
        #     self.close()
        #     sys.exit()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.set_main_window_properties()
        self.create_menubar()
        self.set_app_defaults()
        self.create_dock_widget()


    def create_widgets(self):
        self.textedit = Qtw.QTextEdit()
        self.status_bar = Qtw.QStatusBar()
        self.charcount_label = Qtw.QLabel("chars: 0")

    def create_layouts(self):
        pass

    def create_connections(self):
        self.textedit.textChanged.connect(lambda: self.charcount_label.setText("chars: "+str(len(self.textedit.toPlainText()))))


    def set_main_window_properties(self):
        self.setCentralWidget(self.textedit)
        self.setStatusBar(self.status_bar)
        self.statusBar().addPermanentWidget(self.charcount_label)

    def create_menubar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")
        help_menu = menubar.addMenu("Help")

        # File Menu Actions
        open_action = file_menu.addAction("Open")
        save_action = file_menu.addAction("Save")
        quit_action = file_menu.addAction("Quit", self.close)

        # Edit Menu Actions
        undo_action = edit_menu.addAction("Undo")
        redo_action = edit_menu.addAction("Redo")

        # Help Menu Actions
        about_action = help_menu.addAction("About")

        # Actions Trigger
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        undo_action.triggered.connect(self.textedit.undo) 
        redo_action.triggered.connect(self.textedit.redo) 
        about_action.triggered.connect(self.show_about_dialog)

        # icons
        open_icon = self.style().standardIcon(Qtw.QStyle.SP_DirOpenIcon)
        save_icon = self.style().standardIcon(Qtw.QStyle.SP_DriveHDIcon)
        quit_icon = self.style().standardIcon(Qtw.QStyle.SP_DialogCloseButton)
        open_action.setIcon(open_icon)
        save_action.setIcon(save_icon)
        quit_action.setIcon(quit_icon)

        toolbar = self.addToolBar("File")
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addAction(quit_action)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setAllowedAreas(Qtc.Qt.TopToolBarArea | Qtc.Qt.BottomToolBarArea)

        toolbar_2 = Qtw.QToolBar("Edit")
        toolbar_2.addAction("Copy", self.textedit.copy)
        toolbar_2.addAction("Cut", self.textedit.cut)
        toolbar_2.addAction("Paste", self.textedit.paste)
        toolbar_2.addAction("Font", self.set_font)
        self.addToolBar(Qtc.Qt.RightToolBarArea, toolbar_2)

    def create_dock_widget(self):
        dock = Qtw.QDockWidget("Replace")
        self.addDockWidget(Qtc.Qt.LeftDockWidgetArea, dock)
        dock.setFeatures(Qtw.QDockWidget.DockWidgetMovable | Qtw.QDockWidget.DockWidgetFloatable)

        replace_widget = Qtw.QWidget()
        replace_widget.setLayout(Qtw.QVBoxLayout())
        dock.setWidget(replace_widget)

        self.search_text_input = Qtw.QLineEdit(placeholderText="Search")
        self.replace_text_input = Qtw.QLineEdit(placeholderText="Replace")
        search_replace_btn = Qtw.QPushButton("Search and Replace", clicked=self.search_and_replace)
        replace_widget.layout().addWidget(self.search_text_input)
        replace_widget.layout().addWidget(self.replace_text_input)
        replace_widget.layout().addWidget(search_replace_btn)
        replace_widget.layout().addStretch()

    def search_and_replace(self):
        s_text = self.search_text_input.text()
        r_text = self.replace_text_input.text()

        if s_text:
            self.textedit.setText(self.textedit.toPlainText().replace(s_text, r_text))

    def set_app_defaults(self):
        self.status_bar.showMessage("Welcome to Text Editor")

    def show_about_dialog(self):
        Qtw.QMessageBox.about(self, "About Text Editor", "This is a text editor written in PySide2")

    def open_file(self):
        title = "Select a File to Open...."
        path = Qtc.QDir.homePath()
        filters = "Text Files (*.txt) ;;Python Files(*.py) ;;All Files(*)"
        default_filter = "Python Files(*.py)"
        flags = Qtw.QFileDialog.DontUseNativeDialog | Qtw.QFileDialog.DontResolveSymlinks

        filename, _ = Qtw.QFileDialog.getOpenFileName(self, title, path, filters, default_filter, flags)
        if filename:
            try:
                with open(filename, "r") as fh:
                    self.textedit.setText(fh.read())
            except Exception as e:
                Qtw.QMessageBox.critical(self, "Critical", f"Could not load file: {e}")

    def save_file(self):
        title = "Select a File to Save to...."
        path = Qtc.QDir.homePath()
        filters = "Text Files (*.txt) ;;Python Files(*.py) ;;All Files(*)"

        filename, _ = Qtw.QFileDialog.getOpenFileName(self, title, path, filters)
        if filename:
            try:
                with open(filename, "w") as fh:
                    fh.write(self.textedit.toPlainText())
            except Exception as e:
                Qtw.QMessageBox.critical(self, "Critical", f"Could not save file: {e}")

    def set_font(self):
        current = self.textedit.currentFont()
        accepted, font = Qtw.QFontDialog.getFont(current, self, options=(Qtw.QFontDialog.DontUseNativeDialog | Qtw.QFontDialog.MonospacedFonts))
        if accepted:
            self.textedit.setCurrentFont(font)

if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())