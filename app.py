from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivymd.uix.label import MDLabel
import socket
import threading
import time
import kivy.properties as kyprops


FORMATO = 'utf-8'

def handleMsg(client,self):

  profile = self.root.get_screen("profile")
  chatLog = profile.ids["chatLog"]
  progress2 = profile.ids["progress2"]
  while(True):
    msg = client.recv(1024).decode()
    if(msg.startswith("timer=")):
      chatLog.add_widget(MDLabel(markup=True,text="ta contando",size_hint_y=None,height=24))
      progress2.value = float(msg.split("=")[1])
    else:
      chatLog.add_widget(MDLabel(markup=True,text=msg,size_hint_y=None,height=24))


class LoginScreen(Screen):
  pass



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
      self.root.current = 'profile'
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
      chatInput = profile.ids.chatInput.text
      profile.ids.chatInput.text = ""
      self.client.send(chatInput.encode(FORMATO))
      time.sleep(0.2)


MainApp().run()