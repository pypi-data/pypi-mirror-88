from ConfigDelivery.CCA6.LoadConfiguration import loadConfiguration
from ConfigDelivery.CCA6.DeliveryConfig import DeliveryConfig
import os.path

class DataDelivery():
    '''
    API for CCA6 Data Delivery
    '''

    CCA6_DATA_DIR = r"Cart6.{}productionTSTdata"
    CCA6_DELIVERY_DIR = r"Cart6.{}productionTSTdata\DataDelivery"

    def __init__(self, serialNum = None):
        '''
        Constructor
        '''
        self.reset()
        connectionInfo = loadConfiguration()
        self.filesRoot = connectionInfo['filesroot']
        self.deliveryConfig = DeliveryConfig()
        self.deliverables = self.deliveryConfig.getDeliverables()
        self.setSerialNum(serialNum)
          
    def reset(self):
        '''
        reset the things which get modified when the serialNum changes
        '''
        self.delvierables = None
        self.serialNum = None
        self.dataDir = None
        self.deliveryDir = None        
    
    def setSerialNum(self, serialNum):
        self.reset()
        if serialNum:
            self.serialNum = "{:03d}".format(int(serialNum))
            self.dataDir = os.path.join(self.filesRoot, self.CCA6_DATA_DIR.format(self.serialNum)) 
            self.deliveryDir = os.path.join(self.filesRoot, self.CCA6_DELIVERY_DIR.format(self.serialNum))
            for deliverable in self.deliverables:
                deliverable['dataFile'] = deliverable['dataLocation'].replace('xxx', self.serialNum)
                deliverable['dataFullPath'] = os.path.join(self.dataDir, deliverable['dataFile'])
                deliverable['dataPathValid'] = os.path.exists(deliverable['dataFullPath'])
                
    def getDeliverablesList(self):
        return [{'name' : deliverable['name'],
                 'enable' : deliverable['enable'],
                 'dataLocation' : deliverable['dataLocation']
                } for deliverable in self.deliverables if deliverable['dataPathValid']]
