import io
import threading
import time
from functools import partial

import numpy as np
from cv2 import imdecode

from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.graphics.texture import Texture
from kivy.uix.video import Video
from kivy.uix.label import Label

Builder.load_file('livestream.kv')

class LiveStream(Video):

    # Vision AI
    aiModel = None
    processThisFrame = True
    t_process_frame = None
    bboxFactor = 0
    frameCount = 0
    streamSize = (1280, 720)
    database = None
    databaseIDs = []
    databaseVectors = []

    def __init__(self, model = None, database = None, **kwargs):
        super().__init__(**kwargs)
        self.state = "stop"
        self.source = ""
        self.texture = Texture.create()
        # Vision AI Model
        self.aiModel = model
        # Get data from database
        self.database = database
        if self.database:
            self.get_id_vector(self.database)
        # For bounding box size auto size
        self.bind(size = self.calculate_bbox_factor)

    def get_id_vector(self, db):
        # Get ID from database
        self.databaseIDs.clear()
        self.databaseVectors.clear()
        for key in db.keys():
            self.databaseIDs.append(key)
            # Face vector is at index 2
            self.databaseVectors.append(db[key][2])

    def vector_distance_to_db(self, sample_vector, db_vectors):
        # Return list of distance from sample vector to every vectors in db_vectors list
        distances = []
        for vector in db_vectors:
            # Euclidean distance
            distance = sum(np.power((sample_vector - vector), 2))
            distance = np.sqrt(distance)
            distances.append(distance)
        return distances

    def find_closest_distance(self, distances):
        # Find the smallest value in distance and return the value and its index
        nearest = min(distances)
        index = np.argmin(distances)
        return nearest, index

    def find_vector_id(self, vectors, db_vectors):
        # Return the value in databaseIDs property which index is the index of nearest vector in databaseVectors property
        ids = []
        nearest = []
        for vector in vectors:
            distances = self.vector_distance_to_db(vector, db_vectors)
            nearest, index = self.find_closest_distance(distances)
            id = self.databaseIDs[index]
            ids.append(id)
        return ids, nearest

    def calculate_bbox_factor(self, *args):
        factor1 = self.width / self.streamSize[0]
        factor2 = self.height / self.streamSize[1]
        self.bboxFactor = min(factor1, factor2)

    def display_detection(self, bboxes, face_id, distance):
        # Display detection bounding boxes and labels
        self.clear_widgets()
        self.canvas.after.clear()
        for i in range(len(bboxes)):
            #if distance > ?
            # Box
            xb, yb, width, height = bboxes[i]*self.bboxFactor
            with self.canvas.after:
                Color (0,0.64,0.91, 1.0)
                Line(rectangle = (self.x+xb, self.y+(self.height-yb), width, -height), width = 1.5)
            # label (first name, last name)
            label = (f'{self.database[face_id[i]][0]} {self.database[face_id[i]][1]}')  
            label = Label(text = (label), font_size = 16, font_family = "arial", halign = 'left', valign = 'middle', color = (0,0.4,1), size_hint = (None, None), size = (100, 40), x = self.x+int(xb), y = self.y+(self.height-int(yb)))
            self.add_widget(label)

    # Video Frame Event Function
    def _on_video_frame(self, *largs):
        super()._on_video_frame(*largs)
        # Adjust size according to texture size ?????
        if self.aiModel:
            if self.processThisFrame:
                data = io.BytesIO()
                self.texture.save(data, flipped = False, fmt = 'png')
                if self.t_process_frame is None:
                    self.t_process_frame = threading.Thread(target = partial(self.process_frame, data))
                    self.t_process_frame.start()
            self.frameCount +=1
            if self.frameCount > 20:
                self.frameCount =0
                self.clear_widgets()
                self.canvas.after.clear()

    def process_frame(self, data):
        self.processThisFrame = False
        buff = np.asarray(bytearray(data.read()))
        img = imdecode(buff, 1)
        # Should check if ai_model exist
        '''Detect and extraction'''
        bboxes, faces = self.aiModel.extract_faces(detector_type = 1, img = img)
        '''Recognition'''
        if any(faces):   # Face detected, proceed to recognition
            # Predict
            face_vectors = self.aiModel.create_face_vectors(faces)
            # Find ID
            face_ids, distance = self.find_vector_id(face_vectors, self.databaseVectors)
            # Display detection
            self.display_detection(bboxes, face_ids, distance)
        # Clearing flag for next process
        self.processThisFrame = True
        self.t_process_frame = None

        '''Old functions for softmax prediction'''
        # self.processThisFrame = False
        # buff = np.asarray(bytearray(data.read()))
        # img = imdecode(buff, 1)
        # ## Face detection 
        # bboxes = self.aiModel.detector.detectMultiScale(img)
        # if len(bboxes)>0:   # Face detected, proceed to recognition
        #     ''' RECOGNITION '''
        #     # Check if AI model exist
        #     if self.aiModel.classifier:
        #         # # Preprocessing
        #         faces = self.process_face(img, bboxes)
        #         # # Find face label
        #         preds = self.predict(faces = faces, model = self.aiModel.classifier)
        #     # # Bounding boxes drawing
        #     self.clear_widgets()
        #     self.canvas.after.clear()
        #     for i in range(len(bboxes)):
        #         # Box
        #         xb, yb, width, height = bboxes[i]*self.bboxFactor
        #         # Label
        #         predindex = np.argmax(preds[i])
        #         print (f'PREDINDEX {predindex}, LED PRED: {str(len(preds))}')
        #         confidence = preds[i][predindex]
        #         if confidence > 0.3:
        #             label = str(self.aiModel.classes[predindex])
        #             print (f'BBOX FACTOR {self.bboxFactor}, self width {self.width}, {self.height}, Texture Width {self.texture.width},{self.texture.height} Xb {xb}, Yb {yb}, width {width}, height {height}')
        #             label = Label(text = str(label), font_size = 16, font_family = "arial", halign = 'left', valign = 'middle', color = (0,0.4,1), size_hint = (None, None), size = (100, 40), x = self.x+int(xb), y = self.y+(self.height-int(yb)))
        #             self.add_widget(label)
        #             with self.canvas.after:
        #                 #Color (0,0.69,0.31, 0.9)
        #                 Color (0,0.64,0.91, 1.0)
        #                 Line(rectangle = (self.x+xb, self.y+(self.height-yb), width, -height), width = 1.5)
        # # Clearing flag for next process
        # self.processThisFrame = True
        # self.t_process_frame = None

    # def process_face(self, img, bboxes):
    #     faces = []
    #     for box in bboxes:
    #         x, y, width, height = box
    #         face = img[y:y+height,x:x+width,::]
    #         factor_y = self.target_size[0] / face.shape[0]
    #         factor_x = self.target_size[1] / face.shape[1]
    #         factor = min (factor_x, factor_y)
    #         face = resize(face, (int(face.shape[0]* factor), int(face.shape[1]*factor)))
    #         diff_y = self.target_size[0] - face.shape[0]
    #         diff_x = self.target_size[1] - face.shape[1]
    #         # Padding
    #         face = np.pad(face, ((diff_y//2, diff_y - diff_y//2), (diff_x//2, diff_x-diff_x//2), (0,0)), 'constant')
    #         face = np.expand_dims(face, axis=0)
    #         face = face/255
    #         #face = np.moveaxis(face, -1, 1)
    #         faces.append(face)
    #     return faces

    # def predict (self, faces, model, model_properties=None):
    #     try:
    #         preds = []
    #         for face in faces:
    #             pred = model.predict(face)[0]#.tolist()
    #             predindex = np.argmax(pred)
    #             #print(f'PREDICTION: pred_shape: {pred.shape}, index: {predindex}, label: {self.aiModel.classes[predindex]}, confidence: {pred[predindex]}')
    #             #result = model.infer({model_properties[0]: face})
    #             #output = result[model_properties[1]]
    #             #vector = output[0]
    #             preds.append(pred)
    #         return preds
    #     except Exception as e:
    #         print (f"{e}: Failure during predict")
