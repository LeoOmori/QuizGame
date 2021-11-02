import socket
import threading
from typing import Text

PORT = 5050
FORMATO = 'utf-8'
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def handleMsg():
    print("hello")
    while(True):
        msg = client.recv(1024).decode()
        print(msg)


def start():
    thread1 = threading.Thread(target=handleMsg)
    thread1.start()
    while(True):
        textMsg = input()
        
        client.send(textMsg.encode(FORMATO))
start()