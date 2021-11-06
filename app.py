from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivymd.uix.label import MDLabel
import socket
import threading
import time
import kivy.properties as kyprops


from funcao import comparaString;

FORMATO = 'utf-8'

def handleMsg(client,self):

  profile = self.root.get_screen("profile")
  chatLog = profile.ids["chatLog"]
  progress2 = profile.ids["progress2"]
  while(True):
    msg = client.recv(1024).decode()
    if(msg.startswith("timer=")):
      # chatLog.add_widget(MDLabel(markup=True,text="ta contando",size_hint_y=None,height=24))
      progress2.value = float(msg.split("=")[1])
    else:
      chatLog.add_widget(MDLabel(markup=True,text=msg,size_hint_y=None,height=24))


class LoginScreen(Screen):
  
  def teste(self):
    apelido = self.ids.apelido.text



class ProfileScreen(Screen):
  pass


# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(ProfileScreen(name='profile'))

class MainApp(MDApp):

    def build(self):
      Config.set('graphics','resizable', False)
      kv = Builder.load_file("app.kv")
      return kv

    

    def createConnection(self):
      self.choosenWord = "avengers"
      login = self.root.get_screen("login")
      self.apelido = login.ids.apelido.text
      self.root.current = 'profile'
      profile = self.root.get_screen("profile")
      titleWord =  profile.ids.titleWord
      titleWord.text = self.choosenWord
      PORT = 5050
      SERVER = "127.0.0.1"
      ADDR = (SERVER, PORT)
      self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.client.connect(ADDR)
      self.gameTimer = 0
      thread1 = threading.Thread(target=handleMsg, args=(self.client,self))
      thread1.start()
    
    def sendMessage(self):
      profile = self.root.get_screen("profile")
      word = profile.ids.chatInput.text
      rate = comparaString(self.choosenWord,word)
      if rate <= 3:
        alertMsg = "[b]"+ self.apelido+ "[/b]" + ":" +"[color=00ff2a]Está Perto[/color]"
        self.client.send(alertMsg.encode(FORMATO))
        return
      chatInput = "[b]"+ self.apelido +"[/b]" + ":" + word
      profile.ids.chatInput.text = ""
      self.client.send(chatInput.encode(FORMATO))
      time.sleep(0.2)


MainApp().run()