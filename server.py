import socket, pickle
import threading
import time

SERVER_IP = "127.0.0.1"
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

players = []


def playerList(players):
    playerList = ""
    for player in players:
        playerList = playerList + player["name"] + ","

    return "playerList:" + playerList 


def broadcast(msg):

    for index,player in enumerate(players):
        try:
            player["conn"].send(msg.encode())
        except socket.error as e:
            players.pop(index)
            print("deletado")
        time.sleep(0.2)

def checkConnection():
    while(True):
        for index,player in enumerate(players):
            try:
                player["conn"].send("bot:test".encode())
            except socket.error as e:
                players.pop(index)
                NewPlayerList = playerList(players)
                broadcast(NewPlayerList)
            time.sleep(0.2)
        time.sleep(1)
        
def getMsg(conn, addr):

    while(True):

        msg = conn.recv(1024).decode(FORMATO)
        code = msg.split(":")[0]

        if code == "name":
            name = msg.split(":")[1]
            players.append({
                "addr":addr,
                "conn":conn,
                "name": name
            })

            NewPlayerList = playerList(players)
            broadcast(NewPlayerList)
            print(NewPlayerList)
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
    threadCheck = threading.Thread(target=checkConnection)
    threadCheck.start()
    while(True):
        conn, addr = server.accept()
        thread1 = threading.Thread(target=getMsg, args=(conn,addr))
        # thread2 = threading.Thread(target=timer)
        # thread2.start()
        thread1.start()

mainServer()