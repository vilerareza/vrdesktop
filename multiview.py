import sqlite3

from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from deviceicon import DeviceIcon
from livebox import LiveBox
from livegridlayout import LiveGridLayout

Builder.load_file("multiview.kv")

class Multiview(BoxLayout):
    # Grid layout for live stream
    liveGrid = ObjectProperty(None)
    # Layout for device selection to stream
    selectionBox = ObjectProperty(None)
    # Selection scroll view
    selectionScroll = ObjectProperty(None)
    # List for live stream objects
    liveBoxes = ListProperty([])
    # List for device selection icons
    deviceIcons = ListProperty([])
    # Application manager class
    manager = ObjectProperty(None)
    # Device icon selection scroll buttons
    selectionNextButton = ObjectProperty(None)
    selectionBackButton = ObjectProperty(None)
    selectionInterval = 4
    # Database
    db = ObjectProperty({'dbName': 'test.db', 'tableName': 'camera'})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.liveGrid = LiveGridLayout (size_hint = (1,1), rows=1, cols=1, spacing = 5)
        self.liveGrid.bind(size = self.adjust_livebox_size)
        #self.add_widget(self.liveGrid)
        # Get devices
        #self.get_items_from_db()

    def icon_touch_action(self, deviceIcon, touch):
        if deviceIcon.collide_point(*touch.pos):
            if deviceIcon.isEnabled:
                if self.liveBoxes[self.deviceIcons.index(deviceIcon)].status != "play":
                    # If the live stream object status is not playing then add #
                    self.show_live_box(deviceIcon)
                else:
                    # If the live stream object status is playing then remove
                    self.remove_live_box(deviceIcon)
            
    def show_live_box(self, deviceIcon):
        if self.liveGrid.nLive == 0:
            # Removing initLabel
            self.liveGrid.hide_initlabel()
        # Start the live steaming object
        self.liveBoxes[self.deviceIcons.index(deviceIcon)].start_live_stream()                    
        # Adjust live grid row and cols for displaying live stream #
        self.liveGrid.nLive +=1
        rowLimit = self.liveGrid.rows**2 + self.liveGrid.rows
        if self.liveGrid.nLive > rowLimit:
            self.liveGrid.rows +=1
        colLimit = self.liveGrid.cols**2
        if (self.liveGrid.nLive > colLimit):
            self.liveGrid.cols +=1
        # Display the live stream object to live grid layout
        self.liveGrid.add_widget(self.liveBoxes[self.deviceIcons.index(deviceIcon)])
        # Adjust the livestream to the size of livebox
        self.adjust_livebox_size()
        print (f'ROWS : {self.liveGrid.rows} COLS : {self.liveGrid.cols}')

    def remove_live_box(self, deviceIcon):
        # Stop live stream object
        self.liveBoxes[self.deviceIcons.index(deviceIcon)].stop_live_stream()
        # Remove live stream object from live grid layout
        self.liveGrid.remove_widget(self.liveBoxes[self.deviceIcons.index(deviceIcon)])
        # Re-adjust live grid rows and cols
        self.liveGrid.nLive -=1
        if self.liveGrid.nLive > 0:
            rowLimit = (self.liveGrid.rows-1)**2 + (self.liveGrid.rows-1)
            if self.liveGrid.nLive <= rowLimit:
                self.liveGrid.rows -=1
            colLimit = (self.liveGrid.cols-1)**2
            if (self.liveGrid.nLive <= colLimit):
                self.liveGrid.cols -=1
            # Adjust the livestream to the size of livebox
            self.adjust_livebox_size()
        print (f'ROWS : {self.liveGrid.rows} COLS : {self.liveGrid.cols}')
        if self.liveGrid.nLive == 0:
            # Showing initLabel
            self.liveGrid.show_initlabel()

    def adjust_livebox_size(self, *args):
        cell_width = ((self.liveGrid.width - self.liveGrid.spacing[0]*(self.liveGrid.cols-1))/
                    self.liveGrid.cols)
        cell_height = ((self.liveGrid.height - self.liveGrid.spacing[0]*(self.liveGrid.rows-1))/
                    self.liveGrid.rows)
        for livebox in self.liveBoxes:
            livebox.adjust_self_size(size = (cell_width, cell_height))
        #print (f'GRID SIZE {self.liveGrid.size}, CELL SIZE {cell_width}, {cell_height}')

    def stop_icons(self):
        for deviceIcon in self.deviceIcons:
            deviceIcon.stop()
        self.selectionBox.clear_widgets()
        self.deviceIcons.clear()

    def stop_streams(self):
        # Stop live streams anyway
        for liveBox in self.liveBoxes:
            liveBox.stop_live_stream()
        # Reset and clearing widgets from liveGrid
        self.liveGrid.clear_widgets()
        self.liveGrid.nLive = 0
        self.liveGrid.rows = 1
        self.liveGrid.cols = 1
        # Clear the list of live stream objects
        self.liveBoxes.clear()

    def stop(self):
        self.stop_streams()
        self.stop_icons()

    def get_data_from_db(self):
        # Clearing previous device stream objects and icons if any
        if len(self.deviceIcons) > 0:
            self.stop()
        # Connect to database
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = "SELECT * FROM "+tableName+""
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        self.create_deviceicon_livebox(cur)
        con.close()

    def create_deviceicon_livebox(self, db_cursor):
        # Read every entry in database
        for entry in db_cursor:
            deviceID = entry [0]
            deviceName = entry[1]
            deviceUrl = entry [2]
            deviceNeuralNet = entry [3]
            # Fill device icon list
            self.deviceIcons.append(DeviceIcon(deviceName = deviceName, deviceUrl = deviceUrl, size_hint = (None, None), size = (181, 45)))
            # Fill live box object list
            if deviceNeuralNet == 1:
                # If device neural net is activated then activate the Vision AI
                aiModel = self.manager.create_vision_ai()
                faceDatabase = self.manager.get_facedatabase()
                if aiModel:
                    # Create livebox with detector and model
                    print (f'MULTIVIEW faceDatabase = {len(faceDatabase)}')
                    self.liveBoxes.append(LiveBox(deviceUrl = deviceUrl, model = aiModel, face_database = faceDatabase ))
                else:
                    print ('Model not exist')
            else:
                # If device neural net is not activate then create livebox without detector and model
                self.liveBoxes.append(LiveBox(deviceUrl = deviceUrl))
        # Add deviceIcon content to selection box
        self.add_deviceicon_to_selectionbox(item_list = self.deviceIcons, container = self.selectionBox)

    def add_deviceicon_to_selectionbox(self, item_list, container):
        for item in item_list:
            container.add_widget(item)
    
    def start_icons(self):
        if (len(self.deviceIcons) > 0):
            for deviceIcon in self.deviceIcons:
                # Start the status checker
                deviceIcon.start_status_checker()
                # Binding the touch down event
                deviceIcon.bind(on_touch_down=self.icon_touch_action)
  
    def selection_next_press(self, button):
        if self.selectionScroll.scroll_x < 1:
            self.selectionScroll.scroll_x += 0.1
            if self.selectionScroll.scroll_x >= 1:
                self.selectionScroll.scroll_x = 1

    def selection_back_press(self, button):
        if self.selectionScroll.scroll_x > 0:
            self.selectionScroll.scroll_x -= 0.1
            if self.selectionScroll.scroll_x <= 0:
                self.selectionScroll.scroll_x = 0
