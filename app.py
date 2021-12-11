from re import template
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivymd.uix.label import MDLabel
import socket
import threading
import time
from kivymd.uix.list import OneLineListItem
from funcao import comparaString;

FORMATO = 'utf-8'


def handleMsg(client,self):
  login = self.root.get_screen("login")
  profile = self.root.get_screen("profile")
  leader = self.root.get_screen("leader")
  chatButton = profile.ids['chatButton']
  chatLog = profile.ids["chatLog"]
  progress2 = profile.ids["progress2"]
  setApelido = "name:" + self.apelido
  self.client.send(setApelido.encode(FORMATO))
  while(True):
    msg = client.recv(1024).decode()
    if(msg.startswith("name:")):
      chatLog.add_widget(MDLabel(markup=True,text=msg.split(":")[1]+" entrou no jogo",size_hint_y=None,height=24))
    elif(msg.startswith("timer=")):
      if self.isLeader or self.isRight:
        chatButton.disabled = True
      else:
        chatButton.disabled = False
      progress2.value = float(msg.split("=")[1])
      if float(msg.split("=")[1]) == 0:
        chatButton.disabled = True
        self.isRight = False
        self.isLeader = False

    elif(msg.startswith("playerList:")):
      pList = msg.split(":")
      allPlayers = pList[1].split(",")
      if self.isWaiting:
        if len(allPlayers) <=2 :
          login.ids.waitingPlayers.clear_widgets()
          for i in allPlayers[:-1]:
            login.ids.waitingPlayers.add_widget(
              MDLabel(size_hint_y=None,height=30,text=i)       
            )
            login.ids.waitingPlayers.add_widget(
              MDLabel(size_hint_y=None,height=30,text="esperando...")       
            )
        else:
          self.root.current = 'profile'
          self.isWaiting = False
          profile.ids.containerList.clear_widgets()
          for i in allPlayers[:-1]:
            profile.ids.containerList.add_widget(
              OneLineListItem(text=i)
            )
      else:
          profile.ids.containerList.clear_widgets()
          for i in allPlayers[:-1]:
            profile.ids.containerList.add_widget(
              OneLineListItem(text=i)
            )
    elif(msg.startswith("leader=")):
      self.root.current = 'leader'
    elif(msg.startswith("palavra=")):
      self.isRight = False
      splitMsg = msg.split("=")
      msgSepareted = splitMsg[1].split(",")
      self.listShowChar = []
      self.choosenWord = msgSepareted[2]
      print("palavraEscolhida" + self.choosenWord)
      profile.ids["Tema"].text = "[b]" + "Tema:"  + "[/b]" + msgSepareted[0] + "\n" + "[b]" + "Pista:" +"[/b]"+ msgSepareted[1]
      word = "_" * len(msgSepareted[2])
      profile.ids["titleWord"].text = word
      self.titleword = msgSepareted[2]
    elif(msg.startswith("showChar=")):
      choosenChar = int(msg.split("=")[1])
      self.listShowChar.append(choosenChar)
      word = "_" * len(self.choosenWord)
      wordAux = list(word)
      choosenAux = list(self.choosenWord)
      for char in self.listShowChar:
        wordAux[char] = choosenAux[char]
      profile.ids["titleWord"].text = "".join(wordAux)
    elif (msg.startswith("LeaderTimer=")):
      leaderProgress = leader.ids["leaderProgress"]
      leaderProgress.value = float(msg.split("=")[1])
      if float(msg.split("=")[1]) == 100:
        self.root.current = 'profile'
        self.isLeader == False
      
    elif(msg.startswith("bot:")):
      pass
    else:
      chatLog.add_widget(MDLabel(markup=True,text=msg,size_hint_y=None,height=24))


class LeaderScreen(Screen):
  pass
class LoginScreen(Screen):
  pass

class ProfileScreen(Screen):
  pass



# Create the screen manager
sm = ScreenManager()
sm.add_widget(LeaderScreen(name='leader'))
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(ProfileScreen(name='profile'))

class MainApp(MDApp):

    def build(self):
      Config.set('graphics','resizable', False)
      kv = Builder.load_file("app.kv")
      return kv

    def createConnection(self):
      self.isWaiting = True
      self.listShowChar = [] 
      self.isRight = False
      self.lockChat = True
      self.isLeader = False
      self.choosenWord = ' '
      login = self.root.get_screen("login")
      self.apelido = ""
      self.apelido = login.ids.apelido.text
      login.ids.submitButton.disabled = True
      if self.apelido == "":
        return
      profile = self.root.get_screen("profile")
      chatButton = profile.ids['chatButton']
      chatButton.disabled = True
      PORT = 5050
      SERVER = "127.0.0.1"
      ADDR = (SERVER, PORT)
      self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.client.connect(ADDR)
      thread1 = threading.Thread(target=handleMsg, args=(self.client,self))
      thread1.start()
    
    def sendMessage(self):
      profile = self.root.get_screen("profile")
      progress2 = profile.ids["progress2"]
      word = profile.ids.chatInput.text
      rate = comparaString(self.choosenWord,word)
      if rate == 0:
        basePoint = 2
        fullPoint = 0
        self.isRight = True
        sucessStr = "[b]"+ self.apelido+ "[/b]" + ":" +"[color=00ff2a]Acertou[/color]"
        self.client.send(sucessStr.encode(FORMATO))
        time.sleep(1)
        fullPoint = basePoint + (100 - progress2.value)/10
        pointStr = "isRight=" + str(int(fullPoint))
        self.client.send(pointStr.encode(FORMATO))
        return 
      elif rate <= 3:
        alertMsg = "[b]"+ self.apelido+ "[/b]" + ":" +"[color=002ea1]Está Perto[/color]"
        self.client.send(alertMsg.encode(FORMATO))
        return
      chatInput = "[b]"+ self.apelido +"[/b]" + ":" + word
      profile.ids.chatInput.text = ""
      self.client.send(chatInput.encode(FORMATO))
      time.sleep(0.2)

    def sendTema(self):
      self.isRight = False
      leader = self.root.get_screen("leader")
      tema = leader.ids.tema.text
      dica = leader.ids.dica.text
      self.isLeader = True
      resposta = leader.ids.resposta.text
      list = "tema=" + tema + "," + dica + "," + resposta
      self.client.send(list.encode(FORMATO))
      self.root.current = 'profile'
            
MainApp().run()