import typing
from PySide2 import QtNetwork as Qtn
from PySide2 import QtCore as Qtc
import PySide2.QtCore


class TcpChatInterface(Qtc.QObject):
    PORT = 7777
    delimiter = "||"
    received = Qtc.Signal(str, str)
    error = Qtc.Signal(str)

    def __init__(self, username, recipient):
        super(TcpChatInterface, self).__init__()

        self.username = username
        self.recipient = recipient
    
        self.listener = Qtn.QTcpServer()
        self.listener.listen(address=Qtn.QHostAddress.Any, port=self.PORT)
        self.listener.acceptError.connect(self.on_error)

        self.listener.newConnection.connect(self.on_connection)

        self.connections = []

    def on_error(self, socket_error):
        error_index = Qtn.QAbstractSocket.staticMetaObject.indexOfEnumerator("SocketError")
        error = Qtn.QAbstractSocket.staticMetaObject.enumerator(error_index).valueToKey(socket_error)
        message = f"There was a network error: {error}"
        self.error.emit(message)

    def on_connection(self):
        connection = self.listener.nextPendingConnection()
        connection.readyRead.connect(self.process_datagram)
        self.connections.append(connection)
