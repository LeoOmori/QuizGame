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
    'choosenWord': '',
    'leaderChoosing': True
}

def restartGame():
    for player in players:
        player["points"] = 0

def sortPlayers(unsortedP):
    newlist = sorted(unsortedP, key=lambda x: x["points"], reverse=True)
    return newlist

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
players = []

def playerList(players):
    playerListArray = ""
    for player in players:
        playerListArray = playerListArray + str(player["points"]) + "    " + player["name"] + ","

    return "playerList:" + playerListArray


def broadcast(msg):
    for index,player in enumerate(players):
        try:
            player["conn"].send(msg.encode())
        except socket.error as e:
            players.pop(index)
            sortedList = sortPlayers(players)
            NewPlayerList = playerList(sortedList)
            broadcast(NewPlayerList)
            print("deletado")
            if len(players) < 3:
                GAME['started'] = False  
                GAME["leaderChoosing"] == False
                broadcast("code=endgame")
        time.sleep(0.2)

def checkConnection():
    while(True):
        for index,player in enumerate(players):
            try:
                player["conn"].send("bot:test".encode())
            except socket.error as e:
                players.pop(index)
                sortedList = sortPlayers(players)
                NewPlayerList = playerList(sortedList)
                broadcast(NewPlayerList)
                print("deletado: on check")
                if len(players) < 3:
                    player
                    GAME['started'] = False  
                    GAME["leaderChoosing"] == False
                    broadcast("code=endgame")
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
            lock.acquire()
            broadcast(newWord)
            lock.release()
            GAME["leaderChoosing"] = False
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
            sortedList = sortPlayers(players)
            NewPlayerList = playerList(sortedList)
            if len(players) >= 3:
                GAME['started'] = True
            lock.acquire()
            broadcast(NewPlayerList)
            lock.release()
            print(NewPlayerList)
        elif action[0] == "isRight":
            for player in players:
                if player["addr"][0] == lider["addr"][0] and player["addr"][1] == lider["addr"][1]:
                    player["points"] = player["points"] + 2
                    print(str(player["points"]) + ":isLeader")
                    sortedList = sortPlayers(players)
                    NewPlayerList = playerList(sortedList)
                    lock.acquire()
                    broadcast(NewPlayerList)
                    lock.release()
                    if(player["points"] >= 10 ):
                        time.sleep(0.5)
                        podiumList = "podium=" + sortedList[0]["name"] + "," + sortedList[1]["name"] + "," + sortedList[2]["name"]
                        GAME['started'] = False
                        GAME["leaderChoosing"] == False
                        restartGame()         
                        NewPlayerList = playerList(players)
                        lock.acquire()
                        broadcast(NewPlayerList)
                        lock.release()     
                        time.sleep(1)                   
                        lock.acquire()
                        broadcast(podiumList)
                        lock.release()
                        time.sleep(5)    
                        GAME["started"] = True
                        GAME["choosenWord"] = ''
                        break
                elif player["addr"][0] == addr[0] and player["addr"][1] == addr[1]:
                    player["points"] = player["points"] + int(action[1])
                    print(str(player["points"]) + ":isRight")
                    sortedList = sortPlayers(players)
                    NewPlayerList = playerList(sortedList)
                    lock.acquire()
                    broadcast(NewPlayerList)
                    lock.release()
                    if(player["points"] >= 10 ):
                        time.sleep(0.5)
                        podiumList = "podium=" + sortedList[0]["name"] + "," + sortedList[1]["name"] + "," + sortedList[2]["name"]
                        GAME['started'] = False  
                        GAME["leaderChoosing"] == False
                        restartGame()
                        NewPlayerList = playerList(players)
                        lock.acquire()
                        broadcast(NewPlayerList)
                        lock.release()  
                        time.sleep(1)
                        lock.acquire()
                        broadcast(podiumList)
                        lock.release()
                        time.sleep(5)
                        GAME["started"] = True
                        GAME["choosenWord"] = ''
                        break
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

def RoundTimer():
    while(True):
        if GAME["leaderChoosing"] == False and GAME['started']:
            listChar = []
            for i in range(100):
                r=random.randint(0,len(GAME["choosenWord"])-1)
                if r not in listChar: listChar.append(r)
            for i in range(10):
                if GAME["started"] == False:
                    break
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