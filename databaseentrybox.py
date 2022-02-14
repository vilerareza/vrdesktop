import os
import uuid
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.clock import Clock
from tkinter import Tk, filedialog

import numpy as np
from cv2 import imwrite

Builder.load_file('databaseentrybox.kv')

class DatabaseEntryBox(FloatLayout):

    newID = ''  # New ID
    newFirstName = ''   # New first name
    newLastName = ''    # New last name
    selectedPath = ''   # Selected image folder path
    selectFolderButton = ObjectProperty(None)
    imageReviewButton = ObjectProperty(None)
    imageLocationText = ObjectProperty(None)
    statusLabel = ObjectProperty(None)

    previewImageLocation = 'images/temp/preview/'

    aiModel = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def button_press_callback(self, widget):
        if widget == self.selectFolderButton:
            widget.source = "images/selectfile_down.png"
        elif widget == self.imageReviewButton:
            widget.source = "images/imagereviewbutton_down.png"
        elif widget == self.ids.review_ok_button:
            widget.source = "images/image_review_ok_button_down.png"
        elif widget == self.ids.review_cancel_button:
            widget.source = "images/image_review_cancel_button_down.png"
    
    def button_release_callback(self, widget):
        if widget == self.selectFolderButton:
            widget.source = "images/selectfile.png"
        elif widget == self.imageReviewButton:
            widget.source = "images/imagereviewbutton_normal.png"
        elif widget == self.ids.review_ok_button:
            widget.source = "images/image_review_ok_button_normal.png"
        elif widget == self.ids.review_cancel_button:
            widget.source = "images/image_review_cancel_button_normal.png"
    
    def show_load_dialog(self, widget):
        root = Tk()
        root.withdraw()
        dirname = filedialog.askdirectory()
        root.destroy()
        if dirname:
            self.load_dir(dirname)

    def load_dir(self, dirname):
        # get selection
        self.ids.image_location_text.text = dirname

    def validate_entry(self, *args):
        isValid = True
        for entry in args:    
            if entry.text == '':
                isValid = False
                entry.background_color = (0.9, 0.7, 0.7)
                #entry.hint_text_color = (0.9, 0.2, 0.2)
                if entry == self.ids.new_id_text:
                    entry.hint_text = 'Enter ID...'
                elif entry == self.ids.first_name_text:
                    entry.hint_text = 'Enter first name...'
                elif entry == self.ids.last_name_text:
                    entry.hint_text = 'Enter last name...'
            else:
                entry.foreground_color = (0.2, 0.2, 0.2)
                entry.background_color = (0.8, 0.8, 0.8)

        return isValid

    def get_entry(self, *args):
        isValid = True
        if self.validate_entry(*args) == True:
            self.newID = self.ids.new_id_text.text
            self.newFirstName = self.ids.first_name_text.text
            self.newLastName = self.ids.last_name_text.text
            self.selectedPath = self.ids.image_location_text.text
            return isValid
        else:
            # Put error message here
            isValid = False
            print ('Some entry is not valid')
            return isValid

    def preview_data(self, *args):
        # Callback funciton for "Data Review Button"
        self.imageReviewButton.disabled = True
        if self.get_entry(*args):
            self.display_status(self.statusLabel, 'loading images...')
            Clock.schedule_once(self.display_preview_data, 0)

    def display_preview_data(self, *args):
        if not (self.aiModel):
            self.aiModel = self.create_vision_ai()
        # Clear previous data in the preview directory and clear delete list anyway
        self.clear_images(self.previewImageLocation, self.ids.review_image_grid)
        # Process the data for review
        if (os.path.isdir(self.selectedPath)):
            # Data path is valid and image file exist
            self.add_text_on_widget(self.ids.review_data_label, f'{self.newID}, {self.newFirstName} {self.newLastName}')  # Printing label to image viewer box
            imageFiles = os.listdir(self.selectedPath)
            # Detect face in every image
            for imageFile in imageFiles:
                filePath = os.path.join(self.selectedPath, imageFile)
                detectionExist = self.create_preview_image(filePath)
            if len(os.listdir(self.previewImageLocation)) > 0:
                # Detection exist
                self.hide_no_face()
                self.draw_image_to_grid(imagePath = self.previewImageLocation, gridLayout = self.ids.review_image_grid)
            else:
                self.add_text_on_widget(self.ids.review_data_label, 'Face Not Detected')  # Printing label to image viewer box
                self.display_no_face()
        else:
            print ('Unable to process. Invalid path or empty folder')
        
        self.display_status(self.statusLabel, '')
        self.imageReviewButton.disabled = False
        

    def create_vision_ai(self):
        try:
            from ai_model import AIModel
            model = AIModel(recognition = False)
            print ('model created')
            return model
        except Exception as e:
            print (f'Error on activating Vision AI {e}')

    def add_text_on_widget(self, widget, text):
        widget.text = text

    def create_preview_image(self, filePath):
        # Random file name
        fileName = uuid.uuid4()
        face = self.aiModel.extract_face(filePath)
        if np.any(face):
            writePath = (f'{self.previewImageLocation}{fileName}.png')
            imwrite(writePath, face)
            return True
        return False

    def draw_image_to_grid(self, imagePath, gridLayout):
        # Locate and adding images
        imageFiles = os.listdir(imagePath)
        if len(imageFiles)>0:
            for imageFile in imageFiles:
                gridLayout.add_widget(Image(source = os.path.join(imagePath, imageFile), size_hint = (None, 1)))

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

    def display_status(self, label, text,*args):
        label.text = text

    def display_no_face(self):
        self.ids.no_face_image.opacity = 1

    def hide_no_face(self):
        self.ids.no_face_image.opacity = 0

