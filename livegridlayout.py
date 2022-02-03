from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.core.window import Window

Builder.load_file('livegridlayout.kv')

class LiveGridLayout(GridLayout):
    nLive = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)