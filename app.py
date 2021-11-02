from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivymd.uix.label import MDLabel
import socket
import threading
import time


FORMATO = 'utf-8'

def handleMsg(client,self):

  profile = self.root.get_screen("profile")
  chatLog = profile.ids["chatLog"]
  while(True):
    msg = client.recv(1024).decode()
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
      login = self.root.get_screen("login")

      if login.ids.apelido.text == "1":
        self.root.current = 'profile'
        PORT = 5050
        SERVER = "127.0.0.1"
        ADDR = (SERVER, PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        thread1 = threading.Thread(target=handleMsg, args=(self.client,self))
        thread1.start()
    
    def sendMessage(self):
      profile = self.root.get_screen("profile")
      chatInput = profile.ids.chatInput.text
      profile.ids.chatInput.text = ""
      self.client.send(chatInput.encode(FORMATO))
      time.sleep(0.2)


MainApp().run()