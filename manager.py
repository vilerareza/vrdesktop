from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

Builder.load_file('manager.kv')

class Manager(BoxLayout):

    headerBar = ObjectProperty(None)
    mainTabs = ObjectProperty (None)
    
    aiModel = None

    database = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_main_tabs()

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

    def create_vision_ai(self):
        if not self.aiModel:
            try:
                from ai_model import AIModel
                self.aiModel = AIModel(recognition = True, model_location = "C:/Users/Reza Vilera/.deepface/loaded_model/vgg_model_loaded.h5")
                print ('model created')
            except Exception as e:
                print (f'Error on activating Vision AI {e}')
        
        return self.aiModel

    def add_to_database(self, data_list):
        # Add new data to the database
        # Extract the data
        iD, firstName, lastName, faceVector, faceData = data_list
        # Adding new data and label to dataset
        self.database[iD] = [firstName, lastName, faceVector, faceData]
    
    def get_database(self):
        return self.database

    def stop(self):
        self.mainTabs.stop()