import socket
import select

HEADER_LEN = 20

HOST = "127.0.0.1"
PORT = 62227
ENCODING = "utf-8"


class IPC:
    def __init__(self):
        self.callback = print
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, message_str, target=None):
        if target is None:
            target = self.socket
        message_str = str(message_str)
        full_message = f'{len(message_str):<{HEADER_LEN}}' + message_str
        # print("sending message:", message_str, "to", target)
        target.send(full_message.encode(ENCODING))

    def receive_message(self, from_socket=None):
        if from_socket is None:
            from_socket = self.socket
        try:
            header = from_socket.recv(HEADER_LEN).decode(ENCODING)
            message_length = int(header)
            data = from_socket.recv(message_length).decode(ENCODING)
            return data
        except (ValueError, ConnectionResetError):
            return False

    def register_callback(self, function):
        self.callback = function


class IPCServer(IPC):
    def __init__(self):
        super().__init__()
        self.sockets_list = [self.socket]
        self.clients = {}
        self.socket.bind((HOST, PORT))
        self.socket.listen()

    def run_server(self):
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            for notified_socket in read_sockets:
                if notified_socket == self.socket:
                    client_socket, client_address = self.socket.accept()
                    name = self.receive_message(client_socket)
                    if name is False:
                        continue
                    self.sockets_list.append(client_socket)
                    self.clients[client_socket] = name
                    print("Accepted connection from", name)
                else:
                    message = self.receive_message(notified_socket)
                    if message is False:
                        print('Closed connection from: {}'.format(self.clients[notified_socket]))
                        self.sockets_list.remove(notified_socket)
                        del self.clients[notified_socket]
                        continue
                    # self.callback(message)
                    for client_socket in self.clients:
                        if client_socket != notified_socket:
                            self.send_message(message, client_socket)
            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]


class IPCClient(IPC):

    def __init__(self, client_name="unnamed"):
        super().__init__()
        self.socket.connect((HOST, PORT))
        self.send_message(client_name)

    def listen(self):
        while True:
            self.callback(self.receive_message())
