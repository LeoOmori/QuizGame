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
        try:
            player["conn"].send(msg.encode())
        except socket.error as e:
            del player
            print("deletado")
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
        
def timer():

    for i in range(30):
        newMsg = "timer="+str(i*3.5)
        broadcast(newMsg)
        time.sleep(1)
    broadcast("timer=0")

def mainServer():
    print("servidor Iniciado!!!!!!")
    server.listen()
    while(True):
        conn, addr = server.accept()
        thread1 = threading.Thread(target=getMsg, args=(conn,addr))
        thread2 = threading.Thread(target=timer)
        thread2.start()
        thread1.start()

mainServer()