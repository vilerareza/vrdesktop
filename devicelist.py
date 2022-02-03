from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.lang import Builder

class DeviceList (FocusBehavior, CompoundSelectionBehavior, StackLayout):

    selectedDevice = ObjectProperty(None)
    isDeviceSelected = BooleanProperty(False)

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
        #node.color = (0,1,0)
        node.image.source = 'images/device_selected7.png'
        node.label.font_size = 16
        node.label.text="[color=ffffff]"+node.deviceName+"[/color]"
        self.selectedDevice = node
        self.isDeviceSelected = True
        print ('Item selected in deviceList')
        return super().select_node(node)
        
    def deselect_node(self, node):
        super().deselect_node(node)
        #node.color = (0,0,0)
        node.image.source = 'images/not_device_selected5.png'
        node.label.font_size = 16
        node.label.text="[color=cccccc]"+node.deviceName+"[/color]"
        # Check if nothing is selected
        print (str(len(self.selected_nodes)))
        if len(self.selected_nodes) > 0:
            print(str(self.selected_nodes[0].deviceName))
        if len(self.selected_nodes) == 0:
            self.isDeviceSelected = False
            print ('nothing is selected')
    
    def clear_selection(self, widget=None):
        return super().clear_selection()

    def on_selected_nodes(self,grid,nodes):
        pass
    
    def activate_neuralnet_to_selected_device(self, deviceInfo, neuralNetActivated):
        if self.selectedDevice:
            self.selectedDevice.neuralNetwork = neuralNetActivated


