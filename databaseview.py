import os
import uuid
import pickle
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from tkinter import Tk, filedialog

from cv2 import imwrite

Builder.load_file('databaseview.kv')

class DatabaseView(BoxLayout):

    manager = ObjectProperty(None)

    dataListTempImageLocation = 'images/temp/datalist/'

    def on_parent(self, *args):
        print ('On Parent')
        self.get_database()

    def add_to_list(self, image_folder, string_data_list): 
        # draw the new data to the database list box object 
        self.ids.database_list_box.add_item(string_data_list = string_data_list, image_folder = image_folder)

    def add_new_data(self, image_folder, data_list):
        #self.add_to_database(database = self.datadict, data_list = data_list)
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
        faceDatabase = self.manager.get_facedatabase()
        dataID = selected_data.dataID
        dataContent = faceDatabase[dataID]
        self.ids.database_info_box.display_data(data_id = dataID, data_content = dataContent)

    def check_id_exist(self, new_id):
        faceDatabase = self.manager.get_facedatabase()
        print (f'CHECK ID: {new_id}')
        for id in faceDatabase.keys():
            print (id)
            if id == new_id:
                print ('CHECK ID true')
                return True
        print ('CHECK ID false')
        return False

    def save_database(self): 
        faceDatabase = self.manager.get_facedatabase()
        if (len(faceDatabase) > 0):
            root = Tk()
            root.withdraw()
            filename = filedialog.asksaveasfilename(defaultextension='.pckl', filetypes= [('pickle files','*.pckl')])
            root.destroy()
            if filename:
                with open(filename, 'wb') as file:
                    pickle.dump(faceDatabase, file)
                # Serialize database location to file
                self.manager.save_database_path(filename)
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

    def display_database(self, database):
        # Clearing buffer and layout
        self.clear_images(self.dataListTempImageLocation, gridLayout = self.ids.database_list_box.databaseListLayout)
        for id in database.keys():
            faceImg = database[id][3][0]   # Only take the first image from the list
            self.create_image_from_np(faceImg, self.dataListTempImageLocation)
            string_data_list = [id, database[id][0], database[id][1]]
            self.add_to_list(self.dataListTempImageLocation, string_data_list)
            # Clearing images in buffer location
            self.clear_images(self.dataListTempImageLocation)

    def load_database(self):
        # File selection
        root = Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(filetypes= [("pickle files","*.pckl")])
        root.destroy()
        if filename:
            # Backup current database first
            faceDatabase = self.manager.get_facedatabase()
            faceDatabase_backup = faceDatabase.copy()
            # Clearing existing dataset
            faceDatabase.clear()
            # Processing selected file
            file = open(filename, "rb")
            try:
                faceDatabase.update(pickle.load(file))
                # Display database
                self.display_database(faceDatabase)
                # Serialize database location to file
                self.manager.save_database_path(filename)
            except Exception as e:
                print(f"{e}: Failed loading dataset. Possible cause: wrong dataset file selected. Database restored")
                faceDatabase.update(faceDatabase_backup)   # Restore database to previous state
                # Display database
                self.display_database(faceDatabase)
            finally:
                faceDatabase_backup = None
        else:
            print("Selection canceled. No data loaded...")
            pass

    def get_database(self):
        # Get and show database from manager
        faceDatabase = self.manager.get_facedatabase()
        self.display_database(faceDatabase)