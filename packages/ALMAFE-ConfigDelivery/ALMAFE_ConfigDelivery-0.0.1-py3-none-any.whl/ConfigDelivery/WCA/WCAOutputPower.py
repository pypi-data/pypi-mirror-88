from ALMAFE.database.DriverMySQL import DriverMySQL as driver
from ConfigDelivery.WCA.LoadConfiguration import loadConfiguration
from FETMSDatabase.TestDataHeader import TestDataHeader

class WCAOutputPower(object):
    '''
    classdocs
    '''
    KEYDATASET_VALUES = {
        # definitions of values for keyDataSet field in WCA_OutputPower table
        'OP_VS_LO' : 1,                 # output power vs LO at max VD
        'OP_VS_VD_FINE_LO_STEPS' : 2,   # output power vs VD for fine LO steps 
        'OP_VS_VD_LOW_MID_HI' : 3       # output power vs VD for low, middle, high LO
    }

    def __init__(self):
        '''
        Constructor
        '''
        connectionInfo = loadConfiguration()
        self.DB = driver(connectionInfo)
        self.TDH = TestDataHeader()

    def getOutputPowerVsVD(self, configId):
        '''
        load all output power vs VD records for the specified WCA configId
        :param configId:int to load
        :return list of list[pol, freqLO, VD0, VD1, power]
                sorted by pol, freqLO, VD0, VD1 
        '''
        q = '''SELECT OP.Pol, OP.FreqLO, OP.VD0, OP.VD1, `Power`
            FROM WCA_OutputPower AS OP JOIN TestData_header AS TDH
            ON OP.fkHeader = TDH.keyId
            WHERE fkFE_Components = {0} AND fkTestData_Type = {1}
            AND (keyDataSet = {2} OR keyDataSet = {3}) 
            ORDER BY Pol, FreqLO, VD0, VD1 ASC;
            '''.format(configId, self.TDH.TEST_DATA_TYPES['WCA_OUTPUTPOWER'], 
                       self.KEYDATASET_VALUES['OP_VS_VD_FINE_LO_STEPS'], self.KEYDATASET_VALUES['OP_VS_VD_LOW_MID_HI'])

        if not self.DB.execute(q):
            return None
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            allRows = [[row[0], row[1], row[2], row[3], row[4]] for row in rows]
        return allRows
    
    def getOutputPowerVsLO(self, configId):
        '''
        load all output power vs LO records for the specified WCA configId
        :param configId:int to load
        :return list of list[pol, freqLO, VD0, VD1, power]
                sorted by pol, freqLO 
        '''
        q = '''SELECT OP.Pol, OP.FreqLO, OP.VD0, OP.VD1, `Power`
            FROM WCA_OutputPower AS OP JOIN TestData_header AS TDH
            ON OP.fkHeader = TDH.keyId
            WHERE fkFE_Components = {0} AND fkTestData_Type = {1} AND keyDataSet = {2}
            ORDER BY Pol, FreqLO ASC;
            '''.format(configId, self.TDH.TEST_DATA_TYPES['WCA_OUTPUTPOWER'], self.KEYDATASET_VALUES['OP_VS_LO'])

        if not self.DB.execute(q):
            return None
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            allRows = [[row[0], row[1], row[2], row[3], row[4]] for row in rows]
        return allRows
                
    def insertOutputPower(self, configId, rows, notes = None):
        if not rows:
            return False
        keyId = self.TDH.insertHeader(self.TDH.TEST_DATA_TYPES['WCA_OUTPUTPOWER'], 
                                      configId, 
                                      self.TDH.TEST_DATA_STATUS['CARTRIDGE_PAI'],
                                      rows[0]['band'], 
                                      timeStamp = rows[0]['timeStamp'], 
                                      notes = notes if notes else "loaded by ConfigDelivery.WCAOutputPower")
        if not keyId:
            return False
        q = "INSERT INTO WCA_OutputPower(fkHeader, keyDataSet, TS, FreqLO, Power, Pol, VD0, VD1, VG0, VG1) VALUES "
        firstTime = True
        for row in rows:
            if firstTime:
                firstTime = False
            else:
                q += ", "
            q += "({0}, {1}, '{2}', {3}, {4}, {5}, {6}, {7}, {8}, {9})".format( \
                keyId, row['dataSet'], row['timeStamp'].strftime(self.DB.TIMESTAMP_FORMAT),
                row['freqLO'], row['power'], row['pol'], 
                row['VD0'], row['VD1'], row['VG0'], row['VG1'])
        return self.DB.execute(q, commit = True)
        