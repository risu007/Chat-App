from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# Global variables
HOST = '192.168.0.103'
PORT = 5503
BUFSIZ = 512
ADDR = (HOST, PORT)
MAX_CONNECTIONS=10

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

persons=[]


def broadcast(msg,prefix=""):
    for person in persons:
        try:
            print(person)
            person.client.send(bytes(prefix,"utf8")+msg)
        except  Exception as e:
            print('[EXCEPTION]',e)


def client_communication(person):
    client=person.client
    name=client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg=f'{name} has joined the chat'
    broadcast(bytes(msg,"utf8"))
    while True:
        try:
            msg=client.recv(BUFSIZ)

            if msg == bytes('quit','utf8'):
                client.close()
                persons.remove(person)
                broadcast(bytes("left the chat",'utf8'),name+" : ")
                print('[DISCONNECTED]',name)
                break
            else:
                print(f'{name}: ',msg.decode("utf8"))
                broadcast(msg,name+" : ")

        except Exception as e:
            print('[Exception]',e)
            break

def wait_for_connection(SERVER):
    while True:
        try:
            client,addr= SERVER.accept()
            person=Person(addr,client)
            persons.append(person)
            print(f'[Connection]{addr} connected to the server at {time.asctime() }')
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print('[Exception]',e)
            break

    print('SERVER CRASH')


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection,args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
