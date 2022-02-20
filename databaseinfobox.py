import os
import uuid
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

import numpy as np
from cv2 import imwrite

Builder.load_file('databaseinfobox.kv')

class DatabaseInfoBox(BoxLayout):

    dataID = ''
    dataContent = []

    dataImageLocation = 'images/temp/content/'

    def display_data(self, data_id, data_content):
        self.dataID = data_id
        self.dataContent = data_content
        self.ids.data_id_text.text = data_id
        self.ids.data_firstname_text.text = self.dataContent[0]
        self.ids.data_lastname_text.text = self.dataContent[1]
        self.display_image(self.dataContent[3])

    def display_image(self, image_list):
        self.clear_images(self.dataImageLocation, self.ids.data_image_grid)
        for image in image_list:
            self.create_data_image(image)
        if len(os.listdir(self.dataImageLocation)) > 0:
            # Image exist
            self.draw_image_to_grid(imagePath = self.dataImageLocation, gridLayout = self.ids.data_image_grid)
        
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

    def create_data_image(self, image):
        # Random file name
        fileName = uuid.uuid4()
        writePath = (f'{self.dataImageLocation}{fileName}.png')
        imwrite(writePath, image)

    def draw_image_to_grid(self, imagePath, gridLayout):
        # Locate and adding images
        imageFiles = os.listdir(imagePath)
        if len(imageFiles)>0:
            for imageFile in imageFiles:
                gridLayout.add_widget(Image(source = os.path.join(imagePath, imageFile), size_hint = (None, 1)))

    def button_press_callback(self, widget):
        if widget == self.ids.data_delete_button:
            widget.source = "images/databaseview/database_delete_down.png"
        elif widget == self.ids.data_edit_button:
            widget.source = "images/databaseview/database_new_down.png"

    def button_release_callback(self, widget):
        if widget == self.ids.data_delete_button:
            widget.source = "images/databaseview/database_delete_normal.png"
        elif widget == self.ids.data_edit_button:
            widget.source = "images/databaseview/database_new_normal.png"