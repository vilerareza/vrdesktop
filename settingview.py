from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from deviceentry import DeviceEntry

from mylayoutwidgets import ColoredBox
from deviceitem import DeviceItem
from devicelist import DeviceList
from deviceinfo import DeviceInfo

import sqlite3

#Builder.load_file("settingview.kv")

class SettingView(BoxLayout):

    db = ObjectProperty({'dbName': 'test.db', 'tableName': 'camera'})
    leftBox = ObjectProperty(None)
    deviceInfo = ObjectProperty(None)
    deviceEntry = ObjectProperty(None)
    listBox = ObjectProperty(None)
    tAddress = ObjectProperty(None)
    tName = ObjectProperty(None)
    bAdd = ObjectProperty(None)
    devices = ListProperty([])
    deviceList = ObjectProperty(None)
    
    def add_to_db (self, deviceEntry, isNewDevice):
        if (isNewDevice == True): 
            dbName = self.db['dbName']
            tableName = self.db['tableName']
            camName = deviceEntry.deviceNameText.text
            camUrl = deviceEntry.deviceUrlText.text
            # Device neural network default to 0
            deviceNeuralNet = str(0)
            # Check if exist
            if not (self.check_name_exist_db(camName)):
                sql = "INSERT INTO "+tableName+" (camName, camUrl, neuralNet) VALUES ('"+camName+"','"+camUrl+"','"+deviceNeuralNet+"')"
                con = sqlite3.connect(dbName)
                cur = con.cursor()
                cur.execute(sql)
                con.commit()
                con.close()
                # Set device entry to icon mode
                deviceEntry.icon_mode()
                # Refresh the device list
                self.refresh_devices()
                deviceEntry.isNewDevice = False
            else:
                deviceEntry.messageLabel.text = "[color=ffd42a]Name already exist ![/color]"
                deviceEntry.isNewDevice = False
                
    def save_to_db(self, deviceInfo, editMode):
        print ('save to db')
        try:
            if editMode == False:
                # User pressed "Save"
                dbName = self.db['dbName']
                tableName = self.db['tableName']
                newDeviceName = str(self.deviceInfo.deviceNameText.text)
                newDeviceUrl = str(self.deviceInfo.deviceUrlText.text)
                deviceNeuralNet = str(self.deviceInfo.neuralNetActivated)
                deviceID = str(self.deviceList.selectedDevice.deviceID)
                sql = "UPDATE "+tableName+" SET camName = '"+newDeviceName+"', camUrl = '"+newDeviceUrl+"', neuralNet = '"+deviceNeuralNet+"' WHERE camID = "+deviceID+""
                print (sql)
                con = sqlite3.connect(dbName)
                cur = con.cursor()
                cur.execute(sql)
                con.commit()
                con.close()
                # Refresh the device list
                self.deviceList.disabled = False
                self.devices.clear()
                # Force Device info to change config
                self.deviceList.clear_selection()
                self.deviceInfo.change_config(self.deviceList, self.deviceList.isDeviceSelected, message = "Changes saved...")
                # Do something with Device List
                self.deviceList.clear_widgets()
                self.get_devices()
                for device in self.devices:
                    self.deviceList.add_widget(device)
                self.deviceInfo.dbDeviceNames = self.get_device_name_db()
                # Re-select the edited device
                # for index, device in enumerate (self.devices):
                #     if device.deviceName == newDeviceName:
                #         print (str(device.deviceName))
                #         self.deviceList.select_node(device)
            else:
                # Disable the device list
                self.deviceList.disabled = True

        except Exception as e:
            print ('Failure on saving to database')
            print (e)

    def remove_from_db(self, widget):
        print ('remove from db')
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        deviceID = str(self.deviceList.selectedDevice.deviceID)
        sql = "DELETE FROM "+tableName+" WHERE camID = "+deviceID+""
        print (sql)
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()
        # Refresh devices
        self.refresh_devices()

    def get_devices(self):
        # Connect to database
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = "SELECT * FROM "+tableName+""
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        for entry in cur:
            deviceID = entry [0]
            deviceName = entry[1]
            deviceUrl = entry [2]
            deviceNeuralNet = entry [3]
            imagePath = "images/not_device_selected5.png"
            self.devices.append(DeviceItem(deviceID = deviceID, deviceName = deviceName, deviceUrl = deviceUrl, neuralNetwork = deviceNeuralNet, imagePath=imagePath, size_hint = (None, None), size = (95,85)))
        con.close()

    def check_name_exist_db(self, name):
        for device in self.devices:
            if (device.deviceName == name):
                return True

    def get_device_name_db (self):
        names = []
        for device in self.devices:
            names.append(device.deviceName)
        return names

    def refresh_devices(self):
        # Refresh the device list
        self.devices.clear()
        # Clear device list widgets
        self.deviceList.clear_widgets()
        self.get_devices()
        for device in self.devices:
            self.deviceList.add_widget(device)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Get devices
        self.get_devices()
        # Initialize layout
        self.leftBox = BoxLayout(orientation = "vertical",size_hint = (1.5,1))
        self.deviceInfo = DeviceInfo (color=(0.5,0.5,0.5))
        self.deviceEntry = DeviceEntry(size_hint = (1, 0.5))
        self.listBox = ColoredBox (color=(0.3,0.3,0.3))

        # Device entry
        self.leftBox.add_widget(self.deviceEntry)
        # Binding on_press event of add button
        self.deviceEntry.bind(isNewDevice = self.add_to_db)

        # Device list
        self.deviceList = DeviceList(spacing = 20, padding = [40])
        self.deviceList.bind(selectedDevice = self.deviceInfo.display_info)
        # Populate device list from database
        for device in self.devices:
            self.deviceList.add_widget(device)
        self.listBox.add_widget(self.deviceList)
        self.leftBox.add_widget(self.listBox)
        self.add_widget(self.leftBox)

        # Device info
        self.deviceInfo.bind(editMode = self.save_to_db)
        self.deviceInfo.removeButton.bind(on_press = self.remove_from_db)
        self.deviceInfo.removeButton.bind(on_press = self.deviceList.clear_selection)
        self.deviceInfo.bind(neuralNetActivated = self.deviceList.activate_neuralnet_to_selected_device)
        self.deviceInfo.dbDeviceNames = self.get_device_name_db()
        self.add_widget(self.deviceInfo)

        # Binding Device Info and Device List
        self.deviceList.bind(isDeviceSelected = self.deviceInfo.change_config)

