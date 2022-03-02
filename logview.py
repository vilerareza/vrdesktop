import os
import uuid
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

import numpy as np
from cv2 import imwrite

Builder.load_file('logview.kv')

class LogView(BoxLayout):

    manager = ObjectProperty(None)

    logListTempImagePath = 'images/temp/loglist/'

    def on_parent(self, *args):
        database = self.get_database()
        #if not self.log:
        log = self.get_log()
        self.display_log(log, database)

    def add_to_list(self, image_folder, string_data_list): 
        # draw the new data to the database list box object 
        self.ids.log_list_box.add_item(string_data_list = string_data_list, image_folder = image_folder)

    def display_data_content(self, selected_data):
        '''
        selected_data is DatabaseItem object with the following properties
            dataID = ''
            dataFirstName = ''
            dataLastName = ''
            dataImage = ObjectProperty(None)
            backgroundImage = ObjectProperty(None)
        '''
        # Retrieve data from log database
        dataID = selected_data.dataID
        detectionIds = self.get_log_detection_id(dataID)
        self.ids.log_content_box.display_data(detectionIds)

    def create_image_from_np(self, np_image, destination):
        uuidName = uuid.uuid4()
        writePath = (f'{destination}{uuidName}.png')
        imwrite(writePath, np_image)

    def clear_images(self, imagesLocation = '', gridLayout = None):
        # Removing image files in temp preview directory 
        if imagesLocation != '':
            images = os.listdir(imagesLocation)
            for image in images:
                os.remove(os.path.join(imagesLocation, image))
        # Clearing displayed images in image viewer grid layout
        if gridLayout:
            gridLayout.clear_widgets()
            gridLayout.nLive = 0

    def display_log(self, log, database):
        # Clearing buffer and layout
        self.clear_images(self.logListTempImagePath, gridLayout = self.ids.log_list_box.logListStack)
        ids = self.get_log_ids(log)
        for id in ids:
            faceImg = database[id][3][0]   # Only take the first image from the list
            self.create_image_from_np(faceImg, self.logListTempImagePath)
            string_data_list = [id, database[id][0], database[id][1]]
            self.add_to_list(self.logListTempImagePath, string_data_list)
            # Clearing images in buffer location
            self.clear_images(self.logListTempImagePath)

    def get_log_detection_id(self, face_id):
        return self.manager.get_log_detection_id(face_id)

    def get_database(self):
        # Get database from manager
        return self.manager.get_facedatabase()

    def get_log(self):
        return self.manager.get_log()

    def get_log_ids(self, log):
        # Get faceID from detection log
        ids = []
        for record in log:
            id = record[0]
            ids.append(id)
        ids = np.unique(ids)
        return ids


    
