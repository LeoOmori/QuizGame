import socket
import threading
import time

SERVER_IP = "127.0.0.1"
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


players = []


def broadcast(msg):

    for player in players:
        player["conn"].send(msg.encode())
        time.sleep(0.2)
        
def getMsg(conn, addr):

    players.append({
        "addr":addr,
        "conn":conn,
    })

    while(True):
        msg = conn.recv(1024).decode(FORMATO)
        if(msg):
            broadcast(msg)

def mainServer():
    print("servidor Iniciado!!!!!!")
    server.listen()
    while(True):
        conn, addr = server.accept()
        thread = threading.Thread(target=getMsg, args=(conn,addr))
        thread.start()

mainServer()