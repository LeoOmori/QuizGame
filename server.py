import socket
import threading
import time

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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

players = []
lider = None

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
        action = msg.split("=")

        if action[0] == "tema":
            theme = action[1].split(',')
            GAME['choosenTheme'] == theme[0]
            GAME['choosenHint'] = theme[1]
            GAME["choosenWord"] = theme[2]
            GAME["leaderChoosing"] = False
        if code == "name":
            name = msg.split(":")[1]
            players.append({
                "addr":addr,
                "conn":conn,
                "name": name,
                "points": 0,
                "isRight": False
            })

            NewPlayerList = playerList(players)
            if len(players) >= 2:
                GAME['started'] = True
            broadcast(NewPlayerList)
            print(NewPlayerList)
        else:
            broadcast(msg)
        
def timer():

    while(True):
        if len(players) > 0 and GAME['started'] and GAME['leaderChoosing']:
            leaderStr = "leader=true"
            lider = players[0]
            lider["conn"].send(leaderStr.encode())
            print(lider)          
            for i in range(10):
                if GAME["leaderChoosing"] == False:
                    break
                newMsg = "LeaderTimer="+str(i*10)
                broadcast(newMsg)
                time.sleep(1)
            broadcast("timer=0")
            players.append(lider)
            players.pop(0)
            GAME['round'] += 1

def RoundTimer():
    while(True):
        if GAME["leaderChoosing"] == False:
            for i in range(10):
                newMsg = "timer="+str(i*10)
                broadcast(newMsg)
                time.sleep(1)
            broadcast("timer=0")
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