import os
import uuid
import random
import pickle
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from tkinter import Tk, filedialog

from cv2 import imread, imwrite

Builder.load_file('databaseview.kv')

class DatabaseView(BoxLayout):

    datadict = {}

    dataListTempImageLocation = 'images/temp/datalist/'

    def add_to_database(self, database, data_list):
        # Add new data to the database
        # Extract the data
        iD, firstName, lastName, faceVector, faceData = data_list
        # Adding new data and label to dataset
        database[iD] = [firstName, lastName, faceVector, faceData]

    def add_to_list(self, image_folder, string_data_list): 
        # draw the new data to the database list box object 
        self.ids.database_list_box.add_item(string_data_list = string_data_list, image_folder = image_folder)

    def add_new_data(self, image_folder, data_list):
        self.add_to_database(database = self.datadict, data_list = data_list)
        self.add_to_list(image_folder = image_folder, string_data_list = data_list[0:3])

    def display_data_content(self, selected_data):
        '''
        selected_data is DatabaseItem object with the following properties
            dataID = ''
            dataFirstName = ''
            dataLastName = ''
            dataImage = ObjectProperty(None)
            backgroundImage = ObjectProperty(None)
        '''
        # Retrieve data from database
        dataID = selected_data.dataID
        dataContent = self.datadict[dataID]
        self.ids.database_info_box.display_data(data_id = dataID, data_content = dataContent)

    def check_id_exist(self, new_id):
        print (f'CHECK ID: {new_id}')
        for id in self.datadict.keys():
            print (id)
            if id == new_id:
                print ('CHECK ID true')
                return True
        print ('CHECK ID false')
        return False

    def save_database(self): 
        if (len(self.datadict) > 0):
            root = Tk()
            root.withdraw()
            filename = filedialog.asksaveasfilename(defaultextension='.pckl', filetypes= [('pickle files','*.pckl')])
            root.destroy()
            if filename:
                with open(filename, 'wb') as file:
                    pickle.dump(self.datadict, file)
            else:
                print("No data saved")
        else:
            print ('Nothing to save. Dataset is empty')

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

    def display_database(self):
        # Clearing buffer and layout
        self.clear_images(self.dataListTempImageLocation, gridLayout = self.ids.database_list_box.databaseListLayout)
        for id in self.datadict.keys():
            faceImg = self.datadict[id][3][0]   # Only take the first image from the list
            self.create_image_from_np(faceImg, self.dataListTempImageLocation)
            string_data_list = [id, self.datadict[id][0], self.datadict[id][1]]
            self.add_to_list(self.dataListTempImageLocation, string_data_list)
            # Clearing images in buffer location
            self.clear_images(self.dataListTempImageLocation)

    def load_database(self):
        # Backup current database first
        datadict_backup = self.datadict.copy()
        # File selection
        root = Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(filetypes= [("pickle files","*.pckl")])
        root.destroy()
        if filename:
            # Clearing existing dataset
            self.datadict.clear()
            # Processing selected file
            file = open(filename, "rb")
            try:
                self.datadict = pickle.load(file)
                # Display database
                self.display_database()
            except Exception as e:
                print(f"{e}: Failed loading dataset. Possible cause: wrong dataset file selected")
                self.datadict = datadict_backup.copy()   # Restore database to previous state
                # Display database
                self.display_database()
            finally:
                datadict_backup = None
        else:
            print("Selection canceled. No data loaded...")
            datadict_backup = None