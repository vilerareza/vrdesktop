from cv2 import CascadeClassifier
from tensorflow.keras import models
import numpy as np
from openvino.inference_engine import IECore

class AIModel():

    detector = None
    classifier = None
    classes = None
    modelLocation = '' #"E:/testimages/facetest/vggface/ir/saved_model.xml"
    ieModelProperties = []

    def __init__(self, recognition = False, ie = False, model_location = '', classes_location = ''):
        # Face detector
        self.detector = CascadeClassifier("haarcascade_frontalface_default.xml")
        self.modelLocation = model_location
        # Classifier
        if recognition:
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