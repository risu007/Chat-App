from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock


class Client:

    HOST = '192.168.0.103'
    PORT = 5503
    BUFSIZ = 512
    ADDR = (HOST, PORT)

    def __init__(self,name):

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(Client.ADDR)
        self.messages=[]
        self.receive_thread = Thread(target=self.receive_messages)
        self.receive_thread.start()
        self.send_messages(name)
        self.lock= Lock()

    def receive_messages(self):

        while True:
            try:
                msg=self.client_socket.recv(Client.BUFSIZ).decode('utf8')
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print('[EXCEPTION]',e)
                break

    def send_messages(self,msg):
        try:
            self.client_socket.send(bytes(msg,'utf8'))
            if msg=='quit':
                self.client_socket.close()
        except Exception as e:
            print('[EXCEPTION] ',e)
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(Client.ADDR)

    def get_messages(self):
        message_copy=self.messages[:]

        self.lock.acquire()
        self.messages=[]
        self.lock.release()

        return message_copy


    def disconnect(self):
        self.send_messages('quit')
