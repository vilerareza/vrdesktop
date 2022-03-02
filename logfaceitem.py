from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('logfaceitem.kv')

class LogFaceItem(ButtonBehavior, FloatLayout):
    selected = BooleanProperty (False)
    dataID = ''
    dateStamp = ''
    timeStamp = ''
    dataImage = ObjectProperty(None)
    backgroundImage = ObjectProperty(None)
    
    def __init__(self, string_data_list, image_path, **kwargs):
        super().__init__(**kwargs)
        self.dataID = string_data_list[0]
        self.dateStamp = string_data_list[1]
        self.timeStamp = string_data_list[2]
        self.ids.date_label.text = self.dateStamp
        self.ids.time_label.text = self.timeStamp 
        self.dataImage.source = image_path