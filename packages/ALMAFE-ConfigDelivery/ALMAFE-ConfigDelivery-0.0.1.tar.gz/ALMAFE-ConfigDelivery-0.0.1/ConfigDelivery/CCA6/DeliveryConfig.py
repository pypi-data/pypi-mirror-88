import os.path
import configparser
import copy

class DeliveryConfig():
    '''
    Class to provide access to the CCA6 Data Delivery control files in ConfigFiles
    '''
    CONFIG_FILES_DIR = r"ConfigDelivery\CCA6\ConfigFiles"
    
    def __init__(self):
        self.reset()
        self.readDeliverablesConfig()
        
    def reset(self):
        self.__deliverables = []    
        
    def getDeliverables(self):
        return copy.copy(self.__deliverables)    
    
    def readDeliverablesConfig(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(self.CONFIG_FILES_DIR, "Deliverables Configuration.ini"))
        self.deliverables = []
        for section in config.sections():
            enable = bool(config.get(section, 'Enable', fallback = True))
            dataType = config.get(section, 'Type', fallback = None)
            dataLocation = config.get(section, 'DataLocation', fallback = '')
            configFileName = config.get(section, 'ConfigFileName', fallback = None)
            outputFileName = config.get(section, 'OutputFileName', fallback = None)
            outputFields = config.get(section, 'Output', fallback = '').split(',')
            # add valid sections to the result:
            if type and configFileName and outputFileName and len(outputFields):
                self.__deliverables.append({
                    'name' : section,
                    'enable' : enable,
                    'dataType' : dataType,
                    'dataLocation' : dataLocation,
                    'configFileName' : configFileName,
                    'outputFileName' : outputFileName,
                    'outputFields' : outputFields
                })
                
    def readDataFormatFile(self, deliverable):
        # check for supported dataType:
        dataType = deliverable['dataType'] 
        if not (dataType == 'Excel' or dataType == 'Pattern'):
            print("Unsupported deliverable type '{}'".format(dataType))
            return False
        
        # drop keyBand, keyDataSet, fkCartAssy:
        outputFields = deliverable['outputFields'][3:]
        
        # parse the referenced configFile:
        config = configparser.ConfigParser()
        config.read(os.path.join(self.CONFIG_FILES_DIR, deliverable['configFileName']))
        
        deliveryItems = []
        
        for section in config.sections():
            sheetName = config.get(section, 'Sheetname', fallback = '')
            macro = config.get(section, 'Macro', fallback = '')
            if dataType == 'Excel':
                valuesLocations = []
                for key in outputFields:
                    value = config.get(section, key, fallback = '').strip()
                    if not value:
                        print("Section '{}' is missing key '{}'".format(section.name, key))
                    else:
                        if value[0] == '!':
                            valuesLocations.append({
                                'key' : key,
                                'location' : value[1:],
                                'value' : ''
                            })
                        else:
                            valuesLocations.append({
                                'key' : key,
                                'location' : '',
                                'value' : value
                            })
                deliveryItems.append({
                    'sheetName' : sheetName,
                    'macro' : macro,
                    'valuesLocations' : valuesLocations
                })
            else:
                # dataType == 'Pattern'
                value = config.get(section, 'PatternKeys', fallback = '').strip()
                if not value:
                    print("Section '{}' is missing key 'PatternKeys'".format(section.name))
                else:
                    if value[0] == '!':
                        deliveryItems.append({
                            'sheetName' : sheetName,
                            'macro' : macro,
                            'valuesLocations' : [{'key' : 'PatternKeys', 'location' : value[1:], 'value' : ''}]
                        })
                    else:
                        deliveryItems.append({
                            'sheetName' : sheetName,
                            'macro' : macro,
                            'valuesLocations' : [{'key' : 'PatternKeys', 'location' : '', 'value' : value}]
                        })
        return deliveryItems
            
                
                            
                            
                         
    
    