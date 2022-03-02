import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

import pickle

import sqlite3

Builder.load_file('manager.kv')

class Manager(BoxLayout):

    headerBar = ObjectProperty(None)
    mainTabs = ObjectProperty (None)
    
    aiModel = None

    faceDatabase = {}
    faceDbPath = 'data/databasepath.pckl'

    logDb = {'dbName': 'log.db', 'tableName': 'facelog'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_main_tabs()
        self.load_facedatabase()
        #self.clear_log()

    def move_main_tabs(self):
        ''' Move main tabs to header bar'''
        # Copy the original tabs
        self.newTabs = self.mainTabs.tab_list.copy()
        # Remove the original tabs
        self.mainTabs.clear_tabs()
        self.mainTabs.tab_height = 0
        # Put the copy of original tabs in the 
        for newTab in reversed(self.newTabs):
            # Styling
            if newTab == self.mainTabs.tabSettingView: #ids.id_tab_setting_view:
                # New setting tab
                newTab.size_hint = (None, None)
                newTab.size = (dp(60), dp(40))
                newTab.background_normal = 'images/tab_setting_normal.png'
                newTab.background_down = 'images/tab_setting_down.png'
                self.headerBar.tabStrip.add_widget(newTab)
            elif newTab == self.mainTabs.tabMultiView: #ids.id_tab_multi_view:
                # New multiview tab
                newTab.size_hint = (None, None)
                newTab.size = (dp(60), dp(40))
                newTab.background_normal = 'images/tab_multiview_normal.png'
                newTab.background_down = 'images/tab_multiview_down.png'
                self.headerBar.tabStrip.add_widget(newTab)
            elif newTab == self.mainTabs.tabDatabaseView: 
                # New database tab
                newTab.size_hint = (None, None)
                newTab.size = (dp(60), dp(40))
                newTab.background_normal = 'images/tab_database_normal.png'
                newTab.background_down = 'images/tab_database_down.png'
                self.headerBar.tabStrip.add_widget(newTab)
            elif newTab == self.mainTabs.tabLogView: 
                # New database tab
                newTab.size_hint = (None, None)
                newTab.size = (dp(60), dp(40))
                newTab.background_normal = 'images/tab_log_normal.png'
                newTab.background_down = 'images/tab_log_down.png'
                self.headerBar.tabStrip.add_widget(newTab)

    def create_vision_ai(self):
        if not self.aiModel:
            try:
                from ai_model import AIModel
                self.aiModel = AIModel(recognition = True, model_location = "C:/Users/Reza Vilera/.deepface/loaded_model/vgg_model_loaded.h5")
                print ('model created')
            except Exception as e:
                print (f'Error on activating Vision AI {e}')
        
        return self.aiModel

    def load_facedatabase(self):
        try:
            # Get path to last database
            with open(self.faceDbPath, 'rb') as file:
                databasePath = pickle.load(file)
            # Open the face database
            with open(databasePath, 'rb') as file:
                self.faceDatabase.update(pickle.load(file))
            print ('database loaded')
        except Exception as e:
            print(f"{e}: Failed loading dataset. Possible cause: Face database not exist")
            pass

    def add_to_facedatabase(self, data_list):
        # Add new data to the face database
        # Extract the data
        iD, firstName, lastName, faceVector, faceData = data_list
        # Adding new data to face database
        self.faceDatabase[iD] = [firstName, lastName, faceVector, faceData]
    
    def get_facedatabase(self):
        return self.faceDatabase
    
    def get_vision_ai(self):
        return self.aiModel

    def save_database_path(self, filepath):
        # Serialize database location to file
        with open(self.faceDbPath, 'wb') as file:
            pickle.dump(filepath, file)
    
    def log_detection(self, face_id, detection_id):
        con = sqlite3.connect(self.logDb['dbName'])
        cur = con.cursor()
        sql = "INSERT INTO "+self.logDb['tableName']+" (faceID, detectionID) VALUES ('"+face_id+"', '"+detection_id+"')"
        cur.execute(sql)
        con.commit()
        con.close()

    def clear_log(self):
        con = sqlite3.connect(self.logDb['dbName'])
        cur = con.cursor()
        sql = "DELETE FROM "+self.logDb['tableName']
        cur.execute(sql)
        con.commit()
        con.close()
        # Clear images
        images = os.listdir('logs/images/faces/')
        for image in images:
                os.remove(os.path.join('logs/images/faces/', image))
        images = os.listdir('logs/images/frames/')
        for image in images:
                os.remove(os.path.join('logs/images/frames/', image))

    def get_log(self):
        con = sqlite3.connect(self.logDb['dbName'])
        cur = con.cursor()
        sql = "SELECT * FROM "+self.logDb['tableName']
        cur.execute(sql)
        log = []
        for record in cur:
            log.append(record)
        con.close()
        #print (log)
        return log

    def get_log_detection_id(self, face_id):
        # Get and return detectionID of given faceID from database 
        con = sqlite3.connect(self.logDb['dbName'])
        cur = con.cursor()
        sql = "SELECT detectionID FROM "+self.logDb['tableName']+" WHERE faceID = "+face_id
        cur.execute(sql)
        detectionIds = []
        for i in cur:
            detectionIds.append(i)
        con.close()
        return detectionIds
    
    def stop(self):
        self.mainTabs.stop()