import random
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('databaseitem.kv')

class DatabaseItem(ButtonBehavior, FloatLayout):
    selected = BooleanProperty (False)
    dataID = ''
    dataFirstName = ''
    dataLastName = ''
    dataImage = ObjectProperty(None)
    backgroundImage = ObjectProperty(None)
    
    def __init__(self, string_data_list, filePath, **kwargs):
        super().__init__(**kwargs)
        self.dataID = string_data_list[0]
        self.dataFirstName = string_data_list[1]
        self.dataLastName = string_data_list[2]
        self.ids.data_id_label.text = self.dataID
        self.ids.data_firstname_label.text = self.dataFirstName
        self.ids.data_lastname_label.text = self.dataLastName 
        self.dataImage.source = filePath