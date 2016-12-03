#Required External Modules: cython, pygame, kivy

#import kivy
#kivy.require("1.9.1")

#from os import environ

#environ["KIVY_TEXT"] = "pil"

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from os.path import join, isdir, expanduser
from sys import platform
from kivy.lang import Builder
from file import XFolder
import tools
from webscraper import webscraper


current_os = platform


if current_os.startswith("linux"):
    slash = "/"
elif current_os.startswith("win32") or current_os.startswith("cygwin"):
    slash = "\\"
elif current_os.startswith("darwin"):
    slash = "/"
else:
    slash = "/"


Builder.load_string('''
<AppScreen>
    BoxLayout:
        orientation: "horizontal"
        Label:
            text:"blablabla"
            size_hint: None, None
            size: 150,200
        Label:
            text:"bleblelbe"
            size_hint: None, None
            size: 300, 200
    BoxLayout:
        orientation: "vertical"
        id: box_2
        XButton:
            text: 'Selecione a Pasta'
            on_release: root._folder_dialog()
            size_hint: None, None
            size: 150, 50
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
        TextInput:
            text: root.default_folder
            size: 450, 30
            size_hint: None, None
            id: text_input
    BoxLayout:
        orientation: "vertical"
        Label:
            text:"Frequência de Leitura"
            markup: True
            size_hint: None, None
            size: 450, 100
        Spinner:
            text: "30 segundos"
            values: ("30 segundos","15 minutos","1 hora","6 horas","12 horas")
            size: 150,50
            size_hint: None, None
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
    BoxLayout:
        orientation: "horizontal"
        spacing: 50
        ToggleButton:
            text: "Stop" if self.state == "down" else "Start"
            size: 150, 50
            size_hint: None, None
            pos_hint: {"center_y": 0.5, "center_x": 0.5}
            group: "start"
            on_state: root.start(*args)
            
''')

class AppScreen(GridLayout):

    default_folder = expanduser("~") + slash + "Documents"

    global sel_folder
    sel_folder = default_folder
    
    def scrap(self,event):
        print(sel_folder)
        

    def start(self,*args):
        if args[1] == "down":
            global event
            event = Clock.schedule_interval(self.scrap, 0.5)
        if args[1] == "normal":
            global event
            Clock.unschedule(event)
            


    def update_button(self,event):
        self.ToggleButton.text="Stop"

    def _filepopup_callback(self, instance):
            if instance.is_canceled():
                return
            s = 'Path: %s' % instance.path
            s += ('\nSelection: %s' % instance.selection)
            global sel_folder
            self.ids.text_input.text = instance.path
            sel_folder = instance.path

    def _folder_dialog(self):
        XFolder(on_dismiss=self._filepopup_callback, path=expanduser(u'~'))
        
    
    def __init__(self,**kwargs):
        super(AppScreen, self).__init__(**kwargs)

        #Window.clearcolor = (0.7,0.7,0.7,1)
        
        self.cols = 1
        self.size_hint = (None,1)
        self.width = 450

#        self.layout0 = BoxLayout(orientation="horizontal")
#        image0_1 = Label(
#            text="User Name",
#            size=(150,200),
#            size_hint=(None,None)
#            )
#        label0_2 = Label(
#            text="User Name",
#            size=(300,200),
#            size_hint=(None,None)
#            )
#        self.layout0.add_widget(image0_1)
#        self.layout0.add_widget(label0_2)
#        self.add_widget(self.layout0)
#
#        
#        self.layout1 = BoxLayout(orientation="vertical")
#        label1_1 = Label(
#            text="[color=000000]Diretório Destino[/color]",
#            markup = True,
#            size=(450,100),
#            size_hint=(None,None)
#            )
#        directory1_2 = TextInput(
#            text=expanduser("~")+slash+"Documents",
#            size=(450,30),
#            size_hint=(None,None)
#            )
#        self.layout1.add_widget(label1_1)
#        self.layout1.add_widget(directory1_2)
#        self.add_widget(self.layout1)
#
#        self.layout2 = BoxLayout(orientation="vertical")
#        label2_1 = Label(
#            text="[color=000000]Frequência de Leitura[/color]",
#            markup = True,
#            size=(450,100),
#            size_hint=(None,None)
#            )
#        spin2_2 = Spinner(
#            text="30 segundos",
#            values=("30 segundos","15 minutos","1 hora","6 horas","12 horas"),
#            size=(150,50),
#            size_hint=(None,None),
#            pos_hint={"center_x": 0.5}
#            )
#        self.layout2.add_widget(label2_1)
#        self.layout2.add_widget(spin2_2)
#        self.add_widget(self.layout2)
#
#        
#        self.layout3 = BoxLayout(orientation="vertical",spacing=50)
#        start_btn = ToggleButton(
#            text="Start",
#            size=(200,50),
#            size_hint=(None,None),
#            pos_hint={"center_y": 0.5, "center_x": 0.5}
#            )
#        #btn2 = Button(
#        #    text="Pause",
#        #    size=(200,50),
#        #    size_hint=(None,None),
#        #    pos_hint={"center_y": 0.5}
#        #    )
#        self.layout3.add_widget(start_btn)
#        #self.layout3.add_widget(btn2)
#        self.add_widget(self.layout3)
        


class MyApp(App):

    def build(self):
        return AppScreen()


if __name__ == "__main__" :
    MyApp().run()
