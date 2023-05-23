from PySide2 import QtNetwork as Qtn
from PySide2 import QtCore as Qtc


class UdpChatInterface(Qtc.QObject):
    PORT = 7777
    delimiter = "||"
    received = Qtc.Signal(str, str)
    error = Qtc.Signal(str)

    def __init__(self, username):
        super(UdpChatInterface, self).__init__()

        self.username = username

        self.socket = Qtn.QUdpSocket()
        self.socket.bind(address=Qtn.QHostAddress.Any, port=self.PORT)

        self.socket.readyRead.connect(self.process_datagrams)
        self.socket.error.connect(self.on_error)

    def on_error(self, socket_error):
        error_index = Qtn.QAbstractSocket.staticMetaObject.indexOfEnumerator("SocketError")
        error = Qtn.QAbstractSocket.staticMetaObject.enumerator(error_index).valueToKey(socket_error)
        message = f"There was a network error: {error}"
        self.error.emit(message)

    def process_datagrams(self):
        while self.socket.hasPendingDatagrams():
            datagram = self.socket.receiveDatagram()
            raw_message = bytes(datagram.data()).decode("utf-8")

            if self.delimiter not in raw_message:
                continue

            username, message = raw_message.split(self.delimiter, 1)
            self.received.emit(username, message)

    def send_message(self, message):
        msg_bytes = f"{self.username}{self.delimiter}{message}".encode("utf-8")
        self.socket.writeDatagram(Qtc.QByteArray(msg_bytes), Qtn.QHostAddress.Broadcast, self.PORT)