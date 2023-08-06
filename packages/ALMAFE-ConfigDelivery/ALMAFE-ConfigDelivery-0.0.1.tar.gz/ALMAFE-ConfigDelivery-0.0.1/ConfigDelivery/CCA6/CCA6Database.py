'''
CCA-related database operations on the FETMS database 
'''
from ConfigDelivery.CCA6.LoadConfiguration import loadConfiguration
from ALMAFE.database.DriverMySQL import DriverMySQL as driver
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp

class CCA6Database():
    '''
    Wrapper for FETMS database WCA-related tables
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        connectionInfo = loadConfiguration()
        self.DB = driver(connectionInfo)
        
    def getCCA6Config(self, serialNum = None):
        '''
        Load the most recent configuration record(s) for one or more CCA6
        :param serialNum:str if provided find the record for a specific unit.
        :return 
        or None if not found
        '''
        # this query joins ColdCarts to itself in such a way that only the highest matching keyId is found
        q = '''SELECT CC0.keyColdCarts, CC0.SN, CC0.ESN0, CC0.ESN1, CC0.TS FROM ColdCarts AS CC0
                LEFT JOIN ColdCarts AS CC1 ON CC0.SN = CC1.SN AND CC1.keyColdCarts > CC0.keyColdCarts
                WHERE CC1.keyColdCarts IS NULL'''
        if serialNum:
            q += " AND CC0.SN = '{:03d}'".format(int(serialNum))
        q += " ORDER BY CC0.SN DESC;"

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            # return list of dict:            
            return [{'configId' : row[0],
                     'serialNum' : row[1],
                     'ESN' : row[2],
                     'ESN0' : row[2],
                     'ESN1' : row[3],
                     'timeStamp' : makeTimeStamp(row[4])
                    } for row in rows]
