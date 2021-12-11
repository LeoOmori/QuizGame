import socket
import threading
from threading import Lock
import time
import random

lock = Lock()

SERVER_IP = "127.0.0.1"
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

GAME = {
    'started':False,
    'round':1,
    'winner':[],
    'choosenWord': '',
    'choosenTheme': '',
    'choosenHint': '',
    'leaderChoosing': True
}


def sortObj():
    pass

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
players = []

def playerList(players):
    playerList = ""
    for player in players:
        playerList = playerList + str(player["points"]) + "    " + player["name"] + ","

    return "playerList:" + playerList 


def broadcast(msg):
    for index,player in enumerate(players):
        try:
            player["conn"].send(msg.encode())
        except socket.error as e:
            players.pop(index)
            NewPlayerList = playerList(players)
            broadcast(NewPlayerList)
            print("deletado")
        time.sleep(0.2)

def checkConnection():
    while(True):
        for index,player in enumerate(players):
            try:
                player["conn"].send("bot:test".encode())
            except socket.error as e:
                print(e)
            time.sleep(0.5)
        time.sleep(1)
        
def getMsg(conn, addr):

    while(True):
        msg = conn.recv(1024).decode(FORMATO)

        code = msg.split(":")[0]
        action = msg.split("=")

        if action[0] == "tema":
            theme = action[1].split(',')
            GAME["choosenWord"] = theme[2]
            newWord = 'palavra=' + theme[0] + "," + theme[1] + "," + theme[2]
            GAME["leaderChoosing"] = False
            lock.acquire()
            broadcast(newWord)
            lock.release()
        elif code == "name":
            name = msg.split(":")[1]
            players.append({
                "addr":addr,
                "conn":conn,
                "name": name,
                "points": 0,
                "isRight": False
            })
            lock.acquire()
            broadcast("name:" + name)
            lock.release()

            NewPlayerList = playerList(players)
            if len(players) >= 2:
                GAME['started'] = True
            lock.acquire()
            broadcast(NewPlayerList)
            lock.release()
            print(NewPlayerList)
        elif action[0] == "isRight":
            for player in players:
                if player["addr"][0] == lider["addr"][0] and player["addr"][1] == lider["addr"][1]:
                    player["points"] = player["points"] + 2
                    NewPlayerList = playerList(players)
                    lock.acquire()
                    broadcast(NewPlayerList)
                    lock.release()
                    if(player["points"] >= 20 ):
                        GAME['started'] = False                  
                if player["addr"][0] == addr[0] and player["addr"][1] == addr[1]:
                    player["points"] = player["points"] + int(action[1])
                    NewPlayerList = playerList(players)
                    lock.acquire()
                    broadcast(NewPlayerList)
                    lock.release()
                    if(player["points"] >= 30 ):
                        GAME['started'] = False  
        else:
            lock.acquire
            broadcast(msg)
            lock.release
        
def timer():
    while(True):
        if len(players) > 0 and GAME['started'] and GAME['leaderChoosing']:
            leaderStr = "leader=true"
            global lider
            lider = players[0]
            players[0]["conn"].send(leaderStr.encode())          
            for i in range(10):
                if GAME["leaderChoosing"] == False:
                    break
                newMsg = "LeaderTimer="+str((i+1)*10)
                lock.acquire()
                broadcast(newMsg)
                lock.release()
                time.sleep(1)
            players.append(lider)
            players.pop(0)
            GAME['round'] += 1

def RoundTimer():
    while(True):
        if GAME["leaderChoosing"] == False:
            listChar = []
            for i in range(100):
                r=random.randint(0,len(GAME["choosenWord"])-1)
                if r not in listChar: listChar.append(r)
            for i in range(10):
                newMsg = "timer="+str((i+1)*10)
                if ((i+1)*10) == 30:
                    lock.acquire()
                    broadcast("showChar=" + str(listChar[0]))
                    lock.release()
                elif ((i+1)*10) == 50 and len(GAME["choosenWord"]) > 5:
                    lock.acquire()
                    broadcast("showChar=" + str(listChar[1]))
                    lock.release()
                elif ((i+1)*10) == 70 and len(GAME["choosenWord"]) > 5:
                    lock.acquire()
                    broadcast("showChar=" + str(listChar[2]))
                    lock.release()
                lock.acquire()
                broadcast(newMsg)
                lock.release()
                time.sleep(0.2)
            lock.acquire()
            broadcast("timer=0")
            lock.release()
            GAME["leaderChoosing"] = True

def mainServer():
    print("servidor Iniciado!!!!!!")
    server.listen()
    threadCheck = threading.Thread(target=checkConnection)
    threadCheck.start()
    thread2 = threading.Thread(target=timer)
    thread2.start()
    thread3 = threading.Thread(target=RoundTimer)
    thread3.start()
    while(True):
        conn, addr = server.accept()
        thread1 = threading.Thread(target=getMsg, args=(conn,addr))
        thread1.start()

mainServer()