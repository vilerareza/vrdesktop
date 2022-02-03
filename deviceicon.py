import threading
from kivy.network.urlrequest import UrlRequest
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.lang import Builder

Builder.load_file('deviceIcon.kv')

class DeviceIcon(FloatLayout):
    statusImage = ObjectProperty(None)
    deviceName = StringProperty("")
    deviceUrl = StringProperty("")
    deviceLabel = ObjectProperty(None)
    isEnabled = BooleanProperty(True)
    t_status_checker = None
    condition = threading.Condition()
    request_param_check = "?check=1"
    request_param_start = "?start=1"
    request_param_stop = "?stop=1"
    stop_flag = False
    source1 = "http://192.168.0.100:8000/"

    def __init__(self, deviceName, deviceUrl, **kwargs):
        super().__init__(**kwargs)
        self.deviceName = deviceName
        self.deviceUrl = deviceUrl

    def start_status_checker(self):
        #Start the status checker thread
        if not (self.t_status_checker):
           self.t_status_checker = threading.Thread(target = self.check)
           print ('Starting device checker thread')
           self.t_status_checker.start()

    def check_camera(self):
        req = UrlRequest(url=(self.deviceUrl+self.request_param_check), on_success = self.callback_ok, timeout=2, on_error = self.callback_fail, on_failure = self.callback_fail)
        
    def check(self):
        while (not self.stop_flag):
            # if the application exit then break the loop
            with self.condition:
                if not (self.condition.wait(timeout = 2)):
                    # Timeout. No frame detected
                    self.check_camera()
        # Stop the thread
        if (self.t_status_checker):
            #self.t_status_checker.join (timeout = 0.5)
            self.t_status_checker = None

    def callback_ok(self, request, result):
        #print ("callback OK is called")
        # Enable the item
        self.isEnabled = True
        self.statusImage.source = "images/play.png"
        self.deviceLabel.text = "[color=cccccc]"+self.deviceName+"[/color]"
        
    def callback_fail(self,request, result):
        #print('callback fail called')
        # Disable the frame
        #self.isEnabled = False
        self.statusImage.source = "images/play.png"
        self.deviceLabel.text = "[color=777777]"+self.deviceName+"[/color]"

    def stop(self):
        self.stop_flag=True
