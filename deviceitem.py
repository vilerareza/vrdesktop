import random
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from mylayoutwidgets import ColorLabel

class DeviceItem(FloatLayout):
    deviceID = NumericProperty(0)
    deviceName = StringProperty("")
    deviceUrl = StringProperty("")
    image = ObjectProperty(None)
    label = ObjectProperty(None)
    color = ObjectProperty((0,0,0))
    neuralNetwork = NumericProperty(0)

    def __init__(self, deviceID, deviceName, deviceUrl, imagePath, neuralNetwork, **kwargs):
        super().__init__(**kwargs)
        #self.orientation = 'vertical'
        self.padding = [10]
        self.spacing = 10
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.deviceUrl = deviceUrl
        self.neuralNetwork = neuralNetwork
        self.image = Image (source=imagePath, mipmap = True, size_hint = (1,1), pos_hint = {'center_x':0.5, 'center_y':0.5})
        self.label = ColorLabel(text="[color=dddddd]"+deviceName+"[/color]", font_size = 16, font_family = "arial", halign = "center", valign = "top", size_hint = (None, None), size = (80,25), pos_hint = {'center_x':0.5, 'top': 1}, markup = True)
        #self.deviceLabel = Label(text = "", font_size = 18, font_family = "arial", halign = 'center', valign = 'middle', size_hint = (None, None), size = (120,40), pos_hint = {'center_x':0.5, 'center_y': 0.5}
        self.add_widget (self.image)
        self.add_widget (self.label)
    #     with self.canvas.before:
    #         Color(self.color[0],self.color[1],self.color[2])
    #         #Color(random.random(),random.random(),random.random())
    #         self.rect = Rectangle (pos=self.pos, size = self.size)
    #         self.bind (pos = self.update_rect, size = self.update_rect)
    
    # def update_rect(self, *args):
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size
