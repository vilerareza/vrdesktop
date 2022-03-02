import os
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.uix.behaviors import FocusBehavior

from logfaceitem import LogFaceItem

Builder.load_file('logcontentbox.kv')

class LogContentBox(BoxLayout):

    faceImagePath = 'logs/images/faces/'
    frameImagePath = 'logs/images/frames/'

    def display_data(self, detection_ids):
        self.clear_images(layouts = [self.ids.face_image_stack, self.ids.frame_image_float])
        for detectionId in detection_ids:
            stringDataList = [detectionId, 'test_date', 'test_time']
            self.ids.face_image_stack.add_widget(LogFaceItem(string_data_list = stringDataList, image_path = f'{self.faceImagePath}{detectionId[0]}.png'))

    def clear_images(self, layouts = []):
        for layout in layouts:
            layout.clear_widgets()

    def show_frame(self, detection_id):
        self.ids.frame_image_float.add_widget(Image(source = f'{self.frameImagePath}{detection_id[0]}.png', size_hint = (0.9, 0.9), pos_hint = {'center_x' : 0.5, 'center_y' : 0.5}))

class FaceImageStack (FocusBehavior, CompoundSelectionBehavior, StackLayout):

    myroot = ObjectProperty(None)
    selectedData = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(selectedData = self.inform_selection)

    def inform_selection(self, layout, selected_data):
        detectionId = selected_data.dataID
        self.myroot.show_frame(detectionId)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True
        if self.select_with_key_down(window, keycode, text, modifiers):
            return True
        return False

    def keyboard_on_key_up(self, window, keycode):
        if super().keyboard_on_key_up(window, keycode):
            return True
        if self.select_with_key_up(window, keycode):
            return True
        return False

    def add_widget(self, widget):
        super().add_widget(widget)
        widget.bind(on_touch_down = self.widget_touch_down, on_touch_up = self.widget_touch_up)
    
    def widget_touch_down(self, widget, touch):
        if widget.collide_point(*touch.pos):
            self.select_with_touch(widget, touch)
    
    def widget_touch_up(self, widget, touch):
        if self.collide_point(*touch.pos) and (not (widget.collide_point(*touch.pos) or self.touch_multiselect)):
            self.deselect_node(widget)
    
    def select_node(self, node):
        node.backgroundImage.source = 'images/logview/faceitem_down.png'
        self.selectedData = node
        return super().select_node(node)
        
    def deselect_node(self, node):
        super().deselect_node(node)
        node.backgroundImage.source = 'images/logview/faceitem_normal.png'
    
    def clear_selection(self, widget=None):
        return super().clear_selection()

    def on_selected_nodes(self,grid,nodes):
        pass