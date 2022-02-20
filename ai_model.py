from tensorflow.keras import models
import numpy as np
from openvino.inference_engine import IECore

from cv2 import imread, resize
import numpy as np

class AIModel():

    detector1 = None
    detector2 = None
    classifier = None
    classes = None
    modelLocation = '' #"E:/testimages/facetest/vggface/ir/saved_model.xml"
    ieModelProperties = []

    def __init__(self, recognition = False, ie = False, model_location = '', classes_location = ''):
        
        # Face detector 1 (haarcascade)
        from cv2 import CascadeClassifier
        self.detector1 = CascadeClassifier("haarcascade_frontalface_default.xml")
        # Face detector 2 (mtcnn)
        from mtcnn.mtcnn import MTCNN
        self.detector2 = MTCNN()

        # Classifier
        if recognition:
            self.modelLocation = model_location
            if model_location != '':
                if ie:
                    # Use intel inference engine
                    self.classifier = self.create_inference_engine(self.modelLocation)
                else:
                    # Use regular tf / keras model
                    self.classifier = models.load_model(self.modelLocation)
            else:
                print ('Model location is not set')
        
        if classes_location != '':
            try:
                self.classes = np.load(classes_location)
            except Exception as e:
                print (f'{e}: Failed loading classes')
                self.classes = None
    
    def create_inference_engine(self, model_location):
        ie = IECore()
        net  = ie.read_network(model = model_location)
        input_name = next(iter(net.input_info))
        output_name = next(iter(net.outputs))
        self.ieModelProperties = input_name, output_name
        try:
            model = ie.load_network(network = self.ieModelLocation, device_name = "MYRIAD")
            print ("USE NCS2 VPU")
        except:
            model = ie.load_network(network = self.ieModelLocation, device_name = "CPU")
            print ("NCS2 not found, use CPU...")
        
        return model
    
    def extract_primary_face(self, detector_type, image_path, target_size = (224,224)):
        # Check type of detector
        if detector_type == 1:
            detector = self.detector1
        elif detector_type == 2:
            detector = self.detector2

        img, box = self.detect_primary_face(detector, image_path)
        if np.any(box):
            x1, y1, width, height = box
            x2, y2 = x1 + width, y1 + height
            # face data array
            face = img[y1:y2, x1:x2]
            # Resizing
            factor_y = target_size[0] / face.shape[0]
            factor_x = target_size[1] / face.shape[1]
            factor = min (factor_x, factor_y)
            face_resized = resize(face, (int(face.shape[0]* factor), int(face.shape[1]*factor)))
            diff_y = target_size[0] - face_resized.shape[0]
            diff_x = target_size[1] - face_resized.shape[1]
            # Padding
            face_resized = np.pad(face_resized,((diff_y//2, diff_y - diff_y//2), (diff_x//2, diff_x-diff_x//2), (0,0)), 'constant')
            # Progress
            return face_resized
        return None


    def detect_primary_face(self, detector, image_path):
        img = imread(image_path)

        if detector == self.detector1:
            # Haarcascade detector perform here
            img = imread(image_path)
            bboxes = self.detector.detectMultiScale(img)
            if (len(bboxes)>0):
                # Face detected
                print ('Detector 1: Face detected')
                box = bboxes[0]
                return img, box
            else:
                return img, None

        elif detector == self.detector2:
            # Haarcascade detector perform here
            detection = detector.detect_faces(img)
            if (len(detection)>0):
                print ('Detector 2: Face detected')
                box = detection[0]['box']
                return img, box
            else:
                return img, None

    def make_classifier(self, ie = False, model_location = ''):
        self.modelLocation = model_location
        if self.modelLocation != '':
            if ie:
                # Use intel inference engine
                self.classifier = self.create_inference_engine(self.modelLocation)
            else:
                # Use regular tf / keras model
                self.classifier = models.load_model(self.modelLocation)
            return True
        else:
            print ('Model location is not set')
            return False