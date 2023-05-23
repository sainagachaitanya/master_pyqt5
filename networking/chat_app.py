import sys
from PySide2 import QtWidgets as Qtw
from PySide2 import QtGui as Qtg
from PySide2 import QtCore as Qtc
from udp_chat import UdpChatInterface

class MainWindow(Qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.cw = ChatWindow()
        self.setCentralWidget(self.cw)

        username = Qtc.QDir.home().dirName()
        self.interface = UdpChatInterface(username)
        self.cw.submitted.connect(self.interface.send_message)
        self.interface.received.connect(self.cw.write_message)
        self.interface.error.connect(lambda x: Qtw.QMessageBox.critical(None, "Error", x))


class ChatWindow(Qtw.QWidget):
    submitted = Qtc.Signal(str)

    def __init__(self):
        super(ChatWindow, self).__init__()

        self.setLayout(Qtw.QGridLayout())

        self.message_view = Qtw.QTextEdit()
        self.message_view.setReadOnly(True)
        self.layout().addWidget(self.message_view, 1, 1, 1, 2)

        self.message_entry = Qtw.QLineEdit()
        self.layout().addWidget(self.message_entry, 2, 1)

        self.send_btn = Qtw.QPushButton("Send", clicked=self.send)
        self.layout().addWidget(self.send_btn, 2, 2)

    def write_message(self, username, message):
        self.message_view.append(f"<b>{username}: </b> {message}<br>")

    def send(self):
        message = self.message_entry.text().strip()
        if message:
            self.submitted.emit(message)
            self.message_entry.clear()

if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())