import os
from kivy.properties import BooleanProperty, ObjectProperty 
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.uix.behaviors import FocusBehavior

from databaseitem import DatabaseItem

Builder.load_file('databaselistbox.kv')

class DatabaseListBox(BoxLayout):

    databaseListLayout = ObjectProperty(None)
    saveFile = BooleanProperty(False)
    deleteFile = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_item(self, string_data_list, image_folder):
        imageFiles = os.listdir(image_folder)
        # Display first image only
        filePath = os.path.join(image_folder, imageFiles[0])
        self.databaseListLayout.add_widget(DatabaseItem(string_data_list, filePath))

    def button_press_callback(self, widget):
        if widget == self.ids.database_delete_button:
            widget.source = "images/databaseview/database_delete_down.png"
        elif widget == self.ids.database_new_button:
            widget.source = "images/databaseview/database_new_down.png"
        elif widget == self.ids.database_load_button:
            widget.source = "images/databaseview/database_load_down.png"
        elif widget == self.ids.database_save_button:
            widget.source = "images/databaseview/database_save_down.png"

    def button_release_callback(self, widget):
        if widget == self.ids.database_delete_button:
            widget.source = "images/databaseview/database_delete_normal.png"
        elif widget == self.ids.database_new_button:
            widget.source = "images/databaseview/database_new_normal.png"
        elif widget == self.ids.database_load_button:
            widget.source = "images/databaseview/database_load_normal.png"
        elif widget == self.ids.database_save_button:
            widget.source = "images/databaseview/database_save_normal.png"

    def save_database(self):
        App.get_running_app().manager.mainTabs.databaseView.save_database()
    
    def load_database(self):
        App.get_running_app().manager.mainTabs.databaseView.load_database()


class DatabaseListLayout (FocusBehavior, CompoundSelectionBehavior, StackLayout):

    selectedData = ObjectProperty(None)
    isDataSelected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(selectedData = self.inform_selection)

    def inform_selection(self, layout, selected_data):
        App.get_running_app().manager.mainTabs.databaseView.display_data_content(selected_data)

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
        node.backgroundImage.source = 'images/databaseview/databaseitem_selected.png'
        self.selectedData = node
        self.isDataSelected = True
        return super().select_node(node)
        
    def deselect_node(self, node):
        super().deselect_node(node)
        node.backgroundImage.source = 'images/databaseview/databaseitem_normal.png'
        # Check if nothing is selected
        if len(self.selected_nodes) == 0:
            self.isDataSelected = False
    
    def clear_selection(self, widget=None):
        return super().clear_selection()

    def on_selected_nodes(self,grid,nodes):
        pass
