from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout

from functools import partial

from mylayoutwidgets import ColorLabel
from mylayoutwidgets import ButtonBinded
from mylayoutwidgets import TextInputBinded
from mylayoutwidgets import ImageButton

#Builder.load_file("deviceinfo.kv")

class DeviceEntry(FloatLayout):

    buttonAdd = ObjectProperty(None)
    titleLabel = ObjectProperty()
    deviceNameLabel = ObjectProperty(None)
    deviceUrlLabel = ObjectProperty(None)
    deviceNameText = ObjectProperty(None)
    deviceUrlText = ObjectProperty(None)
    entryMode = BooleanProperty(False)
    widget_x_offset = NumericProperty(0.2)
    saveButton = ObjectProperty(None)
    cancelButton = ObjectProperty(None)
    messageLabel = ObjectProperty(None)
    frontLabel = ObjectProperty(None)

    isNewDevice = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize widgets
        self.buttonAdd = ImageButton(size_hint = (0.4, 0.4), pos_hint = {'center_x':0.5, 'center_y': 0.5}, source = 'images/add2.png')
        self.titleLabel = ColorLabel(text ='New Device', font_size = 24, font_family = "arial", halign = 'left', valign = 'middle', pos_hint = {'x':self.widget_x_offset, 'top': 0.95}, size_hint = (None, None), size = (200, 40))
        self.deviceNameLabel = ColorLabel(text ='Name:', font_size = 16, font_family = "arial", halign = 'left', valign = 'middle', pos_hint = {'x':self.widget_x_offset}, size_hint = (None, None), size = (100, 40))
        self.deviceNameText = TextInputBinded(disabled = False, text = '', font_size = 18, font_family = "arial", multiline = False, size_hint = (None,None), size = (180, 40), pos_hint = {'x':self.widget_x_offset})
        self.deviceUrlLabel = ColorLabel(text ='Url:', font_size = 16, font_family = "arial", halign = 'left', valign = 'middle', size_hint = (None, None), size = (100, 40))
        self.deviceUrlText = TextInputBinded(disabled = False, text = '', font_size = 18, font_family = "arial", multiline = False, size_hint = (None,None), size = (250, 40))
        self.saveButton = ButtonBinded (text = 'Save', size_hint = (None, None), size = (80, 40))
        self.cancelButton = ButtonBinded (text = 'Cancel', size_hint = (None, None), size = (80, 40))
        self.messageLabel = ColorLabel(text ='', font_size = 14, font_family = "arial", halign = 'left', valign = 'middle', pos_hint = {'x':self.widget_x_offset}, size_hint = (None, None), size = (200, 40), markup = True)
        self.frontLabel = ColorLabel(text ='[color=aaaaaa]Add New Device[/color]', font_size = 14, font_family = "arial", halign = 'left', valign = 'middle', pos_hint = {'center_x':0.5}, size_hint = (None, None), size = (100, 40), markup = True)
        # Button callback
        self.buttonAdd.bind(on_press = self.entry_mode)
        self.saveButton.bind(on_press = self.on_save)
        self.cancelButton.bind(on_press = self.icon_mode)
        # Positioning
        # deviceNameLabel
        self.titleLabel.bind(y = (partial(self.deviceNameLabel.update_y_position, offset = 30)))
        self.deviceNameLabel.bind(y = (partial(self.deviceNameText.update_y_position, offset = 30)))
        # URL Label positioning
        # y follow the deviceNameLabel.y
        self.deviceNameLabel.bind(y = (partial(self.deviceUrlLabel.update_y_position, offset = 0)))
        # x offset the deviceNameText.right
        self.deviceNameText.bind(right = (partial(self.deviceUrlLabel.update_x_position, offset = 40)))
        # URL Text positioning
        # y follow the deviceNameText.y
        self.deviceNameText.bind(y = (partial(self.deviceUrlText.update_y_position, offset = 0)))
        # x offset the deviceNameText.right
        self.deviceNameText.bind(right = (partial(self.deviceUrlText.update_x_position, offset = 40)))
        # Cancel Button positioning
        # x follow the deviceUrlText.right
        self.deviceUrlText.bind(right = self.cancelButton.align_right)
        # y follow offset from deviceUrlText.y
        self.deviceUrlText.bind(y = (partial(self.cancelButton.update_y_position, offset = (self.deviceUrlText.height+15))))
        # Save Button positioning
        # x offset from cancelButton.x
        self.cancelButton.bind(x = (partial(self.saveButton.update_x_position, offset = - 90)))
        # y follow the cancelButton.y
        self.cancelButton.bind(y = (partial(self.saveButton.update_y_position, offset = 0)))
        # Message Label positioning
        # y follow the saveButton.y
        self.saveButton.bind(y = (partial(self.messageLabel.update_y_position, offset = 0)))
        # Front Label positioning
        # x offset from buttonAdd.x
        self.buttonAdd.bind(x = (partial(self.frontLabel.update_x_position, offset = 0)))
        # y follow the buttonAdd.y
        self.buttonAdd.bind(y = (partial(self.frontLabel.update_y_position, offset = 40)))
        # Set initial view to icon mode
        self.icon_mode()

    def entry_mode(self, widget):
        # Clear and release widget
        self.clear_widgets()
        # Add widgets
        self.add_widget(self.titleLabel)
        self.add_widget(self.deviceNameLabel)
        self.add_widget(self.deviceNameText)
        self.add_widget(self.deviceUrlLabel)
        self.add_widget(self.deviceUrlText)
        self.add_widget(self.saveButton)
        self.add_widget(self.cancelButton)
        self.add_widget(self.messageLabel)

    def icon_mode(self, widget = None):
        # Clear and release widgets
        self.clear_widgets()
        self.add_widget(self.buttonAdd)
        self.add_widget(self.frontLabel)
        self.deviceNameText.text = ""
        self.deviceUrlText.text = ""
        self.messageLabel.text = ""

    def on_save(self, button):
        if (str(self.deviceNameText.text) != "") and (str(self.deviceUrlText.text)!=""):
            self.isNewDevice = True
