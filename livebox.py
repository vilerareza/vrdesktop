from functools import partial
from threading import Thread

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.behaviors.hover_behavior import HoverBehavior
from kivymd.uix.floatlayout import MDFloatLayout

from audioconnection import AudioReceiver, AudioTransmitter
from mylayoutwidgets import ColorFloatLayout

from livestream import LiveStream

Builder.load_file('livebox.kv')

class LiveBox(MDFloatLayout, HoverBehavior):

    deviceUrl = ''
    liveStream = ObjectProperty(None)
    liveActionBar = ObjectProperty(None)
    moveLeft = ObjectProperty(None)
    moveRight = ObjectProperty(None)
    moveUp = ObjectProperty(None)
    moveDown = ObjectProperty(None)
    status = StringProperty("stop")
    moveEvent = None
    # test stream url
    testUrl = "images/test.mp4"
    moveEnabled = True
    # servo parameter
    servo_center_pos = 7
    servo_max_move = 1.7
    # Audio object
    audioReceiver = None
    audioTransmitter = None

    def __init__(self, model = None, deviceUrl = '', face_database = None, **kwargs):
        super().__init__(**kwargs)
        self.deviceUrl = deviceUrl
        if model and face_database:
            self.set_live_stream (model, face_database) 
        
    def on_enter(self, *args):
        self.show_controls()

    def on_leave(self, *args):
        self.hide_controls()

    def set_live_stream (self, model, face_database):
        self.liveStream.set_model_database(model, face_database)

    def start_live_stream (self):
        try:
            self.liveStream.source = self.deviceUrl+"?start=1"
            #self.liveStream.source = self.testUrl
            self.liveStream.reload()
            self.liveStream.state = "play"
            self.status = "play"
        except:
            print ("Error to start live stream...")
    
    def stop_live_stream (self):
        try:
            self.liveStream.state = "stop"
            self.liveStream.source = ""
            self.status = "stop"
            # Stopping the audio stream anyway
            self.stop_audio_in()
            self.stop_audio_out()
            # Reset the live action bar button state
            self.liveActionBar.reset()
        except Exception as e:
            print ("Error to stop live stream...")
            print (e)

    def adjust_self_size(self, size):
        self.size = size
        self.adjust_livestream_size(size)

    def adjust_livestream_size(self, size):
        factor1 = size[0] / self.liveStream.width
        factor2 = size[1] / self.liveStream.height
        factor = min(factor1, factor2)
        target_size = ((self.liveStream.width * factor), (self.liveStream.height * factor))
        self.liveStream.size = target_size     

    def capture_image(self, file_name = ''):
        if file_name =='':
            self.liveStream.texture.save("test.png", flipped = False)

    def show_controls(self):
        self.liveActionBar.opacity  = 0.7
        self.moveLeft.opacity  = 0.7
        self.moveRight.opacity  = 0.7
        self.moveUp.opacity  = 0.7
        self.moveDown.opacity  = 0.7

    def hide_controls(self):
        self.liveActionBar.opacity  = 0
        self.moveLeft.opacity  = 0
        self.moveRight.opacity  = 0
        self.moveUp.opacity  = 0
        self.moveDown.opacity  = 0

    def button_touch_down(self, *args):
        if args[0].collide_point(*args[1].pos):
            if args[0] == self.moveLeft:
                print ('touch down left')
                if not self.moveEvent:
                    args[0].source = 'images/moveleft_down.png'
                    self.start_move_left()    # move once
                    self.moveEvent = Clock.schedule_interval(self.start_move_left, 0.3)
            if args[0] == self.moveRight:
                print ('touch down right')
                if not self.moveEvent:
                    args[0].source = 'images/moveright_down.png'
                    self.start_move_right()    # move once
                    self.moveEvent = Clock.schedule_interval(self.start_move_right, 0.3)
            if args[0] == self.moveUp:
                print ('touch down up')
                if not self.moveEvent:
                    args[0].source = 'images/moveup_down.png'
                    self.start_move_up()    # move once
                    self.moveEvent = Clock.schedule_interval(self.start_move_up, 0.3)
            if args[0] == self.moveDown:
                print ('touch down down')
                if not self.moveEvent:
                    args[0].source = 'images/movedown_down.png'
                    self.start_move_down()    # move once
                    self.moveEvent = Clock.schedule_interval(self.start_move_down, 0.3)

    def button_touch_up(self, *args):
        if args[0].collide_point(*args[1].pos):
            print ('touch up')
            if self.moveEvent:
                self.move_cancel(self.moveEvent)
                self.moveEvent = None
                self.moveLeft.source = 'images/moveleft_normal.png'
                self.moveRight.source = 'images/moveright_normal.png'
                self.moveUp.source = 'images/moveup_normal.png'
                self.moveDown.source = 'images/movedown_normal.png'

    def move_cancel(self, moveEvent = None):
        if moveEvent:
            moveEvent.cancel()
            moveEvent = None
        return

    def move_left(self, distance):
        print ('move left')
        req = UrlRequest(url=(self.deviceUrl+"?left="+str(distance)), timeout=1)

    def move_right(self, distance):
        print ('move right')
        req = UrlRequest(url=(self.deviceUrl+"?right="+str(distance)), timeout=1)

    def move_up(self, distance):
        print ('move up')
        req = UrlRequest(url=(self.deviceUrl+"?up="+str(distance)), timeout=1)

    def move_down(self, distance):
        print ('move down')
        req = UrlRequest(url=(self.deviceUrl+"?down="+str(distance)), timeout=1)
    
    def start_move_left(self, distance = 0.1, *args):
        # Start the move thread
        moveThread = Thread(target = partial(self.move_left, distance))
        moveThread.start()
  
    def start_move_right(self, distance =0.1, *args):
        # Start the move thread
        moveThread = Thread(target = partial(self.move_right, distance))
        moveThread.start()

    def start_move_up(self, distance = 0.1, *args):
        # Start the move thread
        moveThread = Thread(target = partial(self.move_up, distance))
        moveThread.start()
  
    def start_move_down(self, distance =0.1, *args):
        # Start the move thread
        moveThread = Thread(target = partial(self.move_down, distance))
        moveThread.start()

    def on_touch_down(self, touch):
        super().on_touch_down(touch)

        # Movements
        if self.moveEnabled:
            if self.liveStream.collide_point(*touch.pos) and not (
                self.moveLeft.collide_point(*touch.pos) or
                self.moveRight.collide_point(*touch.pos) or
                self.moveUp.collide_point(*touch.pos) or
                self.moveDown.collide_point(*touch.pos)):

                touchPos = (touch.pos[0]-self.liveStream.x, touch.pos[1]-self.liveStream.y)
                # Calculate move distance
                distance_x, distance_y = self.calculate_move_distance(touch_x = touchPos[0], touch_y = touchPos[1])

                if distance_x > 0.1:
                    # Touch is at left area
                    self.start_move_left(abs(distance_x))
                elif distance_x < -0.1:
                    # Touch is at right area
                    self.start_move_right(abs(distance_x))

                if distance_y > 0.1:
                    # Touch is at lower area
                    self.start_move_down(abs(distance_y))
                elif distance_y < -0.1:
                    # Touch is at upper area
                    self.start_move_up(abs(distance_y))

                print (f'touch pos: {touchPos}')

    def calculate_move_distance(self, touch_x=0, touch_y=0):
        distance_x = (((self.liveStream.center_x-self.liveStream.x) - touch_x)/(self.liveStream.center_x-self.liveStream.x)) * self.servo_max_move
        distance_y = (((self.liveStream.center_y-self.liveStream.y) - touch_y)/(self.liveStream.center_y-self.liveStream.y)) * self.servo_max_move
        #print (f'move distance: {distance}, center_x: {self.liveStream.center_x}, touch_x: {touch_x}')
        return distance_x, distance_y

    def start_audio_in(self):
        # Start audio_in
        audioinThread = Thread(target = self.audio_in)
        audioinThread.start()

    def audio_in(self):
        print ('audio_in')
        self.audioReceiver = AudioReceiver(self.deviceUrl, devicePort = 65001)
        self.audioReceiver.start_stream()

    def stop_audio_in(self):
        if self.audioReceiver:
            self.audioReceiver.stop_stream()
            self.audioReceiver = None

    def start_audio_out(self):
        # Start audio_out
        audiooutThread = Thread(target = self.audio_out)
        audiooutThread.start()

    def audio_out(self):
        print ('audio_out')
        self.audioTransmitter = AudioTransmitter(self.deviceUrl, devicePort = 65002)
        self.audioTransmitter.start_stream()

    def stop_audio_out(self):
        if self.audioTransmitter:
            self.audioTransmitter.stop_stream()
            self.audioTransmitter = None
