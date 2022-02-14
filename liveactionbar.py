from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

Builder.load_file('liveactionbar.kv')

class LiveActionBar (GridLayout):
    pass

    def button_press_callback(self, button):
        if button == self.ids.capture_image_button:
            button.source = 'images/capturedown.png'
            if self.parent:
                self.parent.capture_image()
        elif button == self.ids.movement_actionbar_icon:
            button.source = 'images/movement_down.png'
            print('pressed...')
        #manager = App.get_running_app().manager
    
    def button_release_callback(self, button):
        if button == self.ids.capture_image_button:
            button.source = 'images/capturenormal.png'
        if button == self.ids.movement_actionbar_icon:
            button.source = 'images/movement_normal.png'

    def button_touch_action(self, *args):
        if args[0].collide_point(*args[1].pos):
            print ('touch')
    
    def toggle_press_callback(self, button):
        if button == self.ids.speaker_icon_button:
            if button.state == 'down':
                button.source = 'images/speaker_down.png'
                if self.parent:
                    self.parent.start_audio_in()
            else:
                button.source = 'images/speaker_normal.png'
                if self.parent:
                    self.parent.stop_audio_in()
            
        elif button == self.ids.mic_icon_button:
            button.source = 'images/movement_down.png'
            if button.state == 'down':
                button.source = 'images/mic_down.png'
                if self.parent:
                    self.parent.start_audio_out()
            else:
                button.source = 'images/mic_normal.png'
                if self.parent:
                    self.parent.stop_audio_out()
    
    def reset(self):
        self.ids.speaker_icon_button.state = 'normal'
        self.ids.speaker_icon_button.state = 'normal'