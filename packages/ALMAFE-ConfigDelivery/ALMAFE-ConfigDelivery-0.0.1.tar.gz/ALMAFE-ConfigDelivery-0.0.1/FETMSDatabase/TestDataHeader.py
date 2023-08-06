from ALMAFE.database.DriverMySQL import DriverMySQL as driver
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from FETMSDatabase.LoadConfiguration import loadConfiguration

class TestDataHeader(object):
    '''
    classdocs
    '''

    TEST_DATA_TYPES = {
        'WCA_OUTPUTPOWER' : 46
    }
    
    TEST_DATA_STATUS = {
        'UNKNOWN' : 0,
        'COLD_PAS' : 1,
        'WARM_PAS' : 2,
        'COLD_PAI' : 3,
        'HEALTH_CHECK' : 4,
        'CARTRIDGE_PAI' : 7
    }

    def __init__(self):
        '''
        Constructor
        '''
        connectionInfo = loadConfiguration()
        self.DB = driver(connectionInfo)
        
    def insertHeader(self, testDataType, fkFEComponent, dataStatus, band, dataSetGroup = 0, timeStamp = None, notes = None):
        q = "INSERT INTO TestData_header(fkTestData_Type, DataSetGroup, fkFE_Components, fkDataStatus, Band, TS";
        if notes:
            q += ", Notes"
        timeStamp = makeTimeStamp(timeStamp).strftime(self.DB.TIMESTAMP_FORMAT)
        q += ") VALUES ({0}, {1}, {2}, {3}, {4}, '{5}'".format(testDataType, dataSetGroup, fkFEComponent, dataStatus, band, timeStamp)
        if notes:
            q += ", '{0}'".format(notes)
        q += ");"
        if not self.DB.execute(q):
            return False
        self.DB.execute("SELECT LAST_INSERT_ID();")
        row = self.DB.fetchone()
        if not row:
            self.DB.rollback()
            return False
        else:
            self.DB.commit()
            return row[0]
    
    def getHeader(self, testDataType, configId):
        q = '''SELECT keyId, fkTestData_Type, DataSetGroup, fkFE_Components, Band, TS, Notes FROM TestData_header
               WHERE fkTestData_Type = {0} AND fkFE_Components = {1} ORDER BY keyId DESC;'''.format(testDataType, configId)
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            # return list of dict:            
            return [{'keyId' : row[0],
                     'type' : row[1],
                     'group' : row[2],
                     'configId' : row[3],
                     'band' : row[4],
                     'timeStamp' : makeTimeStamp(row[5]),
                     'notes' : row[6]
                    } for row in rows]

    def getHeaderSpecific(self, keyId):
        q = '''SELECT keyId, fkTestData_Type, DataSetGroup, fkFE_Components, Band, TS, Notes FROM TestData_header
               WHERE keyId = {0}
               ORDER BY keyId DESC;'''.format(keyId)
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        else:
            return {'keyId' : row[0],
                    'type' : row[1],
                    'group' : row[2],
                    'configId' : row[3],
                    'band' : row[4],
                    'timeStamp' : makeTimeStamp(row[5]),
                    'notes' : row[6]
                   }

    def deleteHeader(self, testDataType, configId):
        q = '''DELETE FROM TestData_header
               WHERE fkTestData_Type = {0} AND fkFE_Components = {1};'''.format(testDataType, configId)
        self.DB.execute(q, commit = True)
    
    def deleteHeaderSpecific(self, keyId):
        q = "DELETE FROM TestData_header WHERE keyId = {0};".format(keyId)
        self.DB.execute(q, commit = True)
        
    
    
    