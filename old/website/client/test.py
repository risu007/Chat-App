from client import Client
from threading import Thread
import time


c1=Client('x')
c2=Client('y')

def update_messages():
    msgs=[]
    run= True
    while run:
        time.sleep(1)
        new_messages=c1.get_messages()
        msgs.extend(new_messages)
        for message in new_messages:
            print(message)
            if message=='quit':
                run=False
                break

Thread(target=update_messages).start()

c2.send_messages('hello')
time.sleep(1)
c1.send_messages('hw r u')
time.sleep(1)
c2.send_messages('fine')
time.sleep(1)
c1.send_messages('me too')
time.sleep(1)
c1.disconnect()
time.sleep(1)
c2.disconnect()



