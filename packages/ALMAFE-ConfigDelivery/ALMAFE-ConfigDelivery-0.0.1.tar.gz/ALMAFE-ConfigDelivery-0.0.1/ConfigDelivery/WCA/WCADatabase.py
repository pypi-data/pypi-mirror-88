'''
WCA-related database operations on the FETMS database 
'''

from ConfigDelivery.Plot.WCA import PlotWCA
from ConfigDelivery.WCA.LoadConfiguration import loadConfiguration
from ConfigDelivery.WCA.WCAOutputPower import WCAOutputPower
from ALMAFE.database.DriverMySQL import DriverMySQL as driver
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from xml.etree import ElementTree as ET
import os.path
import pandas as pd

class WCADatabase():
    '''
    Wrapper for FETMS database WCA-related tables
    '''
    # define maximum safe LO power allowed per band. 0=no restriction: 
    BAND_MAX_SAFE_POWER_MW = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 40,
        5 : 40,
        6 : 53,
        7 : 53,
        8 : 134,
        9 : 168,
        10 : 168
    }
    # define warm LO multiplication factor per band:
    BAND_WARM_MULT = {
        1 : 1,
        2 : 6,  # this is subject to change for the ESO band 2
        3 : 6,
        4 : 3,
        5 : 6,
        6 : 6,
        7 : 6,
        8 : 3,
        9 : 3,
        10 : 6
    }
    # define lowest LO freq per band:
    BAND_LO_LOWEST = {
        1 : 31.0,
        2 : 79.0,
        3 : 92.0,
        4 : 133.0,
        5 : 167.0,
        6 : 221.0,
        7 : 283.0,
        8 : 393.0,
        9 : 614.0,
        10 : 799.0
    }
    
    def __init__(self):
        '''
        Constructor
        '''
        connectionInfo = loadConfiguration()
        self.DB = driver(connectionInfo)
        self.outputPower = WCAOutputPower()
        self.plotWCA = None
            
    def getWCAConfig(self, band = None, serialNum = None):
        '''
        Load the most recent configuration record(s) for one or more WCAs
        :param band:int if provided, filter by band (1..10)
        :param serialNum:str if provided find the record for a specific unit. Only has effect if band is provided.
        :return list of dict{configId, band, serialNum, ESN, timeStamp, fLoYig, fHiYig, VG0, VG1}
                or None if not found
        '''
        
        # this query joins FE_Components to itself in such a way that only the highest matching keyId is found
        # it also joins WCAs to get the YIG oscillator limits
        q = '''SELECT FEC0.keyId, FEC0.Band, FEC0.SN, FEC0.ESN1, FEC0.TS, WCAs.FloYIG, WCAs.FhiYIG, WCAs.VG0, WCAs.VG1
                FROM FE_Components AS FEC0 LEFT JOIN FE_Components AS FEC1
                ON FEC0.Band = FEC1.Band AND FEC0.SN = FEC1.SN AND FEC1.keyId > FEC0.keyId
                JOIN WCAs ON fkFE_Component = FEC0.keyId
                WHERE FEC1.keyId IS NULL
                AND FEC0.fkFE_ComponentType = 11'''
        
        if band and 1 <= band <= 10: 
            # filter by band:
            q += " AND FEC0.Band = {0}".format(band)
            if serialNum:
                # filter for a specific SN of the provided band
                q += " AND (FEC0.SN = '{:s}' OR FEC0.SN = '{:02d}')".format(str(serialNum), int(serialNum))
        q += " ORDER BY FEC0.keyId;"

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            # return list of dict:            
            return [{'configId' : row[0],
                     'band' : row[1],
                     'serialNum' : row[2],
                     'ESN' : row[3],
                     'timeStamp' : makeTimeStamp(row[4]),
                     'fLoYig' : row[5],
                     'fHiYig' : row[6],
                     'VG0' : row[7],
                     'VG1' : row[8]
                    } for row in rows]

    def getWCAConfigSpecific(self, configId):
        '''
        Load a specific WCA configuration record
        :param configId:int component keyId
        :return dict{configId, band, serialNum, ESN, timeStamp, fLoYig, fHiYig}
                or None if not found
        '''
        q = '''SELECT FEC.keyId, FEC.Band, FEC.SN, FEC.ESN1, FEC.TS, WCAs.FloYIG, WCAs.FhiYIG, WCAs.VG0, WCAs.VG1
                FROM FE_Components AS FEC
                JOIN WCAs ON fkFE_Component = FEC.keyId
                WHERE FEC.keyId = {0}
                AND FEC0.fkFE_ComponentType = 11'''.format(configId)
        
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        else:
            # return dict:
            return {'configId' : row[0],
                    'band' : row[1],
                    'serialNum' : row[2],
                    'ESN' : row[3],
                    'timeStamp' : makeTimeStamp(row[4]),
                    'fLoYig' : row[5],
                    'fHiYig' : row[6],
                    'VG0' : row[7],
                    'VG1' : row[8]}

    def getWCAMaster(self, band = None, serialNum = None):
        '''
        Load the ESN for one or more band/serialNum pairs from the WCA SN to ESN master table
        'WCAMaster_2020_11_10' provided by Jim Muehlberg on 10-November-2020
        :param band:int if provided, filter by band (1..10)
        :param serialNum:str if provided find the record for a specific unit. Only has effect if band is provided.
        :return list of dict{band, serialNum, ESN, timeStamp, fLoYig, fHiYig, VG0, VG1} ordered by band, serialNum
        '''
        q = 'SELECT Band, UnitSerial, ESN, LoTune, HiTune, VG0, VG1 from WCAMaster_2020_11_10'
        if band and 1 <= band <= 10: 
            # filter by band:
            q += " WHERE Band = {0}".format(band)
            if serialNum:
                # filter for a specific SN of the provided band
                q += " AND UnitSerial = '{0}'".format(serialNum)
        q += " ORDER BY Band, UnitSerial;"
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            # return list of dict:            
            return [{'band' : row[0],
                     'serialNum' : row[1],
                     'ESN' : row[2],
                     'timeStamp' : makeTimeStamp("2020-11-10"),
                     'fLoYig' : row[3],
                     'fHiYig' : row[4],
                     'VG0' : row[5],
                     'VG1' : row[6]
                    } for row in rows]

    def getLOParams(self, configIds):
        '''
        Load the LOParams records for one or more configIds
        :param configIds:int or list(int)
        :return list of dict{configId, freqLO, VD0, VD1} 
                or None if not found
        '''
        q = "SELECT fkComponent, FreqLO, VDP0, VDP1 FROM WCA_LOParams"
        q += " WHERE fkComponent in ("
        first = True
        try:
            # try iteration:
            for configId in configIds:
                if first:
                    first = False
                else:
                    q += ","
                q += str(configId)
        except:
            # iteration failed, treat it as a single int:
            q += str(configIds)
        q += ") ORDER BY fkComponent, FreqLO;"
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            # return list of dict:
            return [{'configId' : row[0], 
                     'freqLO' : row[1], 
                     'VD0' : row[2], 
                     'VD1' : row[3]
                    } for row in rows]

    def updateESN(self, configId, ESN):
        q = "UPDATE FE_Components SET ESN1 = '{0}' WHERE keyId = {1}".format(ESN, configId)
        self.DB.execute(q, commit = True)

    def updateYIG(self, configId, fLoYig, fHiYig):
        q = "UPDATE WCAs SET FloYIG = '{0}', FhiYIG = '{1}' WHERE fkFE_Component = {2}".format(fLoYig, fHiYig, configId)
        self.DB.execute(q, commit = True)

    def updateVGs(self, configId, VG0, VG1):
        q = "UPDATE WCAs SET VG0 = '{0}', VG1 = '{1}' WHERE fkFE_Component = {2}".format(VG0, VG1, configId)
        self.DB.execute(q, commit = True)

    def verifyWCA(self, band = None, serialNum = None, updateESN = False, updateYIG = False, updateVGs = False, showProgress = False):
        '''
        Verify that the WCA data in the Components and WCAs tables matches the Master table.
        :param band:int if provided, filter by band (1..10)
        :param serialNum:str if provided find the record for a specific unit. Only has effect if band is provided.
        :param updateESN: if True, repair the Components table ESN to match the Master table
        :param updateYIG: if True, repair the WCAs table YIG endpoints to match the Master table
        :param updateVGs: if True, repair the WCAs table VG0 and VG1 to match the Master table
        :param showProgress: if True, print the WCA SN and status for each item processed
        :return list of dict{band, SN, found:bool, matchESN:bool, matchYIG:bool, matchVGs: bool}
        '''
        configs = self.getWCAConfig(band, serialNum)
        masters = self.getWCAMaster(band, serialNum)
        # loop on masters because it is in band, serialNum order:
        output = []
        for item in masters:                
            found = False
            matchESN = False
            matchYIG = False
            matchVGs = False
            if showProgress:
                print('WCA{}-{:02d} '.format(item['band'], int(item['serialNum'])), end='', flush=True)

            config = None
            if configs:                
                config = next((x for x in configs \
                              if x['band'] == item['band'] \
                              and x['serialNum'].isnumeric() and int(x['serialNum']) == item['serialNum']), None)
            if not config:
                if showProgress:
                    print('not found')
            else:
                found = True
                if config['ESN'] == item['ESN']:
                    matchESN = True
                else:
                    if showProgress:
                        print('ESN mismmatch ', end='', flush=True)
                    if updateESN:
                        self.updateESN(config['configId'], item['ESN'])
                        if showProgress:
                            print('fixed! ', end='', flush=True)

                if config['fLoYig'] == item['fLoYig'] and config['fHiYig'] == item['fHiYig']:
                    matchYIG = True
                else:
                    if showProgress:
                        print('YIG mismmatch ', end='', flush=True)
                    if updateYIG:
                        self.updateYIG(config['configId'], item['fLoYig'], item['fHiYig'])
                        if showProgress:
                            print('fixed! ', end='', flush=True)
                
                if config['VG0'] == item['VG0'] and config['VG1'] == item['VG1']:
                    matchVGs = True
                else:
                    if showProgress:
                        print('VGs mismmatch ', end='', flush=True)
                    if updateVGs:
                        self.updateVGs(config['configId'], item['VG0'], item['VG1'])
                        if showProgress:
                            print('fixed! ', end='', flush=True)

            output.append({'band' : item['band'],
                           'serialNum' : item['serialNum'],
                           'ESN' : item['ESN'],
                           'found' : found,
                           'matchESN' : matchESN,                               
                           'matchYIG' : matchYIG,
                           'matchVGs' : matchVGs
                          })
            if showProgress:
                print('')
        return output
    
    def insertWCA(self, wcaRecord):
        '''
        Insert a record into the FE_Components table and the WCAs table from a dict
        :param wcaRecord: dict{band, serialNum, ESN, timeStamp, fLoYig, fHiYig, VG0, VG1}
        :return bool: indicating success
        '''
        TS = wcaRecord['timeStamp'].strftime(self.DB.TIMESTAMP_FORMAT)
        q = '''INSERT INTO `FE_Components`
                (`fkFE_ComponentType`, `SN`, `ESN1`, `Band`, `TS`) VALUES (11, '{0}', '{1}', {2}, '{3}');
            '''.format(wcaRecord['serialNum'], wcaRecord['ESN'], wcaRecord['band'], TS)
        self.DB.execute(q)
        self.DB.execute("SELECT LAST_INSERT_ID();")
        row = self.DB.fetchone()
        if not row:
            self.DB.rollback()
            return False
        else:
            q = '''INSERT INTO `WCAs` (`TS`, `fkFE_Component`, `FloYIG`, `FhiYIG`, `VG0`, `VG1`)
                    VALUES ('{0}', {1}, {2}, {3}, {4}, {5});
                '''.format(TS, row[0], wcaRecord['fLoYig'], wcaRecord['fHiYig'], wcaRecord['VG0'], wcaRecord['VG1'])
            if self.DB.execute(q):
                self.DB.commit()
                return True
            else:
                self.DB.rollback()
                return False

    def writeXML(self, outputDir, band = None, serialNum = None, showProgress = False, makePlot = False, showPlot = False):
        '''
        create XML data delivery file(s) for one or more WCAs
        optionally create corresponding max safe power plot(s)
        :param outputDir:str path to a directory where the files will be created/replaced
        :param band:int if provided, filter by band (1..10)
        :param serialNum:str if provided find the record for a specific unit.  Only has effect if band is provided.
        :param showProgress: if True write a dot to the console for each file written 
        :param makePlot: if True, generate a plot of the max safe power table
        :param showPlot: if True and makePlot, show the plot interactively
        :raise ValueError: if outputDir doesn't exist
        '''
        if not os.path.exists(outputDir):
            raise ValueError('outputDir does not exist')
        # get the matching WCAConfig records:
        configs = self.getWCAConfig(band, serialNum)
        if configs:
            # loop to create individual WCA files:
            for config in configs:
                self.makeSerialString(config)
                # only create files for WCAs with numeric serial numbers; exclude the test sources, etc:
                doCreate = config['serialNumIsNumeric']
                # don't create files for band 5 pre-production WCAs:
                if doCreate and (config['band'] == 5 and int(config['serialNum']) < 10):
                    doCreate = False
                if doCreate:
                    self.writeConfigXML(outputDir, config, showProgress, makePlot, showPlot)
                    self.writeOutputPowerXML(outputDir, config, showProgress)
        if showProgress:
            print(' done!')

    def makeSerialString(self, config):
        '''
        Make a human-readable serial number string, like 'WCA3-21'
        :param config: dict{configId, band, serialNum, ESN, timeStamp, fLoYig, fHiYig, VG0, VG1}
        :return adds keys 'serialString' and 'serialNumIsNumeric' to config
        '''
        try:
            # for numeric SN strings:
            config['serialString'] = 'WCA{}-{:02d}'.format(config['band'], int(config['serialNum']))
            config['serialNumIsNumeric'] = True
        except:
            # for SN strings containing non-numeric chars:
            config['serialString'] = 'WCA{}-{}'.format(config['band'], config['serialNum'])
            config['serialNumIsNumeric'] = False

    def writeConfigXML(self, outputDir, config, showProgress = False, makePlot = False, showPlot = False):
        '''
        create XML config delivery file for a single WCA
        optionally create corresponding max safe power plot
        :param outputDir:str path to a directory where the file(s) will be created/replaced
        :param config: dict{configId, band, serialNum, serialString, ESN, timeStamp, fLoYig, fHiYig, VG0, VG1}
        :param showProgress: if True write a dot to the console for each file written 
        :param makePlot: if True, generate a plot of the max safe power table
        :param showPlot: if True and makePlot, show the plot interactively
        :raise ValueError: if outputDir doesn't exist        
        '''
        if not os.path.exists(outputDir):
            raise ValueError('outputDir does not exist')

        # build the XML ElementTree:
        top = ET.Element('ConfigData')
        tree = ET.ElementTree(top)
        ET.SubElement(top, 'ASSEMBLY', attrib = {'value' : 'WCA{0}'.format(config['band'])})
        ET.SubElement(top, 'WCAConfig', attrib = {'value' : '{0}'.format(config['configId']), 
                                                  'timestamp' : '{0}'.format(config['timeStamp'].isoformat())})
        ET.SubElement(top, 'ESN', attrib = {'value' : '{0}'.format(config['ESN'])})
        ET.SubElement(top, 'SN', attrib = {'value' : config['serialString']})
        ET.SubElement(top, 'FLOYIG', attrib = {'value' : '{:.3f}E9'.format(config['fLoYig'])})
        ET.SubElement(top, 'FHIYIG', attrib = {'value' : '{:.3f}E9'.format(config['fHiYig'])})
        # not using LOParams here for data delivery.  VDs=0.0 with the correct VGs:
        ET.SubElement(top, 'PowerAmp', attrib = {'FreqLO' : '{:.3f}E9'.format(self.BAND_LO_LOWEST[config['band']]),
                                                 'VD0' : '0.0',
                                                 'VD1' : '0.0',
                                                 'VG0' : '{0}'.format(config['VG0']),
                                                 'VG1' : '{0}'.format(config['VG1'])})
        
        # compute max safe LO power:
        maxSafeTable = self.getMaxSafePowerTable(config) if 4 <= config['band'] <= 10 else None
        if maxSafeTable:
            # write the PowerAmpLimit elements:
            for row in maxSafeTable:
                ET.SubElement(top, 'PowerAmpLimit ', attrib = {'count' : '{0}'.format(int(row['yigTuning'])),
                                                               'VD0' : '{0}'.format(row['VD0']),
                                                               'VD1' : '{0}'.format(row['VD1'])})

        # write the XML file.  Filename is decimal representation of ESN:
        if config['ESN']:
            fileName = '{0}.XML'.format(int(config['ESN'], 16))
        else:
            fileName = '{0}.XML'.format(config['serialString'])
        file = os.path.join(outputDir, fileName)
        tree.write(file, encoding = "ISO-8859-1", xml_declaration = True)
        
        # plot max safe power:
        if makePlot:
            if not self.plotWCA:
                self.plotWCA = PlotWCA()
            limit = self.BAND_MAX_SAFE_POWER_MW[config['band']]
            plotName = '{0}_PowerAmpLimit.PNG'.format(config['serialString'])
            plotName = os.path.join(outputDir, plotName)
            title = "{} max safe power (limit = {} mW)\nfile: '{}'" \
                    .format(config['serialString'], limit, fileName)
            self.plotWCA.plotMaxSafeTable(plotName, maxSafeTable, limit, title, show = showPlot)
        if showProgress:
            print('.', end='', flush=True)
    
    def writeOutputPowerXML(self, outputDir, config, showProgress = False):
        '''
        create XML output power vs LO delivery file for a single WCA
        :param outputDir:str path to a directory where the file will be created/replaced
        :param config: dict{configId, band, serialNum, serialString, ESN, timeStamp, fLoYig, fHiYig, VG0, VG1}
        :param showProgress: if True write a dot to the console for each file written 
        :raise ValueError: if outputDir doesn't exist
        :return True if success, False if no data found or error       
        '''
        if not os.path.exists(outputDir):
            raise ValueError('outputDir does not exist')

        # load all output power vs LO test data:
        allRows = self.outputPower.getOutputPowerVsLO(config['configId'])
        if not allRows:
            return False

        # build the XML ElementTree:
        top = ET.Element('OutputPowerVsLO')
        tree = ET.ElementTree(top)
        ET.SubElement(top, 'ASSEMBLY', attrib = {'value' : 'WCA{0}'.format(config['band'])})
        ET.SubElement(top, 'WCAConfig', attrib = {'value' : '{0}'.format(config['configId']), 
                                                  'timestamp' : '{0}'.format(config['timeStamp'].isoformat())})
        ET.SubElement(top, 'SN', attrib = {'value' : config['serialString']})
        for row in allRows:
            # [pol, freqLO, VD0, VD1, power]
            ET.SubElement(top, 'OutputPower', attrib = {'pol' : '{0}'.format(row[0]),
                                                        'FreqLO' : '{:.3f}E9'.format(row[1]),
                                                        'VD0' : '{0}'.format(round(row[2], 4)),
                                                        'VD1' : '{0}'.format(round(row[3], 4)),
                                                        'powerMW' : '{0}'.format(round(row[4], 1))})
        
        # write out the file:
        fileName = '{0}_OutputPower.XML'.format(config['serialString'])
        file = os.path.join(outputDir, fileName)
        tree.write(file, encoding = "ISO-8859-1", xml_declaration = True)
        if showProgress:
            print('.', end='', flush=True)
        return True
                    
    def getMaxSafePowerTable(self, config):
        '''
        Calculate and return a table of maximum safe LO power settings for the specified config.
        :param config: single WCAConfig object
                   or: single int configId for a specific WCA.
        :return list of dict{freqLO, yigTuning, VD0, VD1, power0, power1}
                sorted by freqLO
        '''
        if isinstance(config, int):
            config = self.getWCAConfigSpecific(config)
        
        # if yigSpan is zero, something is wrong with this config. Get out now:
        yigSpan = config['fHiYig'] - config['fLoYig']
        if yigSpan == 0:
            return None
            
        # get the band-specific power limit.  If 0 skip this:
        limit = self.BAND_MAX_SAFE_POWER_MW[config['band']]
        if not limit:
            return None
            
        # load all output power vs VD test data:
        allRows = self.outputPower.getOutputPowerVsVD(config['configId'])
        # quit now if there's no data:
        if not allRows:
            return None
        allRows = pd.DataFrame(allRows, columns = ['pol', 'freqLO', 'VD0', 'VD1', 'power'])
        # quit now if empty DataFrame:
        if allRows.empty:
            return None

        try:
            # find max output power for each pol:
            f = allRows.groupby(['pol']).max()
            maxVD0 = f.loc[0, 'VD0']
            maxVD1 = f.loc[1, 'VD1']
        except:
            return None
        # compute scaling factors to convert drain voltages into control values:
        if maxVD0 == 0.0 or maxVD1 == 0.0:
            return None
        scaleVD0 = 2.5 / maxVD0
        scaleVD1 = 2.5 / maxVD1
        
        # reduce it to rows holding the max allowed output power:
        allRows = self.findMaxSafeRows(allRows, limit);

        # will divide by the WCA warm multiplication factor:
        warmMult = self.BAND_WARM_MULT[config['band']]

        # loop to scale the YIG tuning and drain voltages:
        f = allRows
        for i in range(0, f.shape[0]):
            f.loc[f.index[i], 'VD0'] = round(f.loc[f.index[i], 'VD0'] * scaleVD0, 4)
            f.loc[f.index[i], 'VD1'] = round(f.loc[f.index[i], 'VD1'] * scaleVD1, 4)
            f.loc[f.index[i], 'power0'] = round(f.loc[f.index[i], 'power0'], 1)
            f.loc[f.index[i], 'power1'] = round(f.loc[f.index[i], 'power1'], 1)
            f.loc[f.index[i], 'yigTuning'] = round((((f.index[i] / warmMult) - config['fLoYig']) / yigSpan) * 4095)
        
        # reset the index to include freqLO, return as a list of dict:
        return allRows.reset_index().to_dict('records')
    
    def findMaxSafeRows(self, allRows, powerLimit):
        '''
        transform result from loadOutputPower() into a table indexed by freqLO
        having the max safe VD0, VD1 to stay under the powerLimit
        and retaining only the endpoints of duplicate sequences on (VD0 AND VD1) 
        :param allRows:pandas.DataFrame[pol, freqLO, VD0, VD1, power]
               sorted by Pol, freqLO, VD0, VD1
        :param powerLimit:float max safe power allowed mW
        :return pandas.DataFrame[freqLO, VD0, power0, VD1, power1]
                sorted by freqLO
        '''
        # for each pol, grouped by freqLO, get the indices of the rows having max power but under the power limit:
        ix0 = allRows[(allRows['power'] <= powerLimit) & (allRows['pol'] == 0)].groupby(['freqLO'])['VD0'].idxmax()
        ix1 = allRows[(allRows['power'] <= powerLimit) & (allRows['pol'] == 1)].groupby(['freqLO'])['VD1'].idxmax()
        # make new DataFrames for pol0 and pol1 from the found indices:        
        msr0 = pd.DataFrame([allRows.loc[x, ['freqLO', 'VD0', 'power']] for x in ix0])
        msr1 = pd.DataFrame([allRows.loc[x, ['freqLO', 'VD1', 'power']] for x in ix1])
        # rename the power columns:
        msr0.rename(columns={"power": "power0"}, inplace = True)
        msr1.rename(columns={"power": "power1"}, inplace = True)
        # set the index to freqLO:        
        msr0.set_index('freqLO', inplace = True)
        msr1.set_index('freqLO', inplace = True)
        # join the two tables, 'outer' in case a freqLO record is missing from one or the other:
        msr = msr0.join(msr1, how='outer')
        # mark all but the endpoints of duplicate ranges over (VD0 AND VD1) with 'dup' = True 
        for i in range(1, msr.shape[0] - 2 + 1):
            # matches prev record?
            dupL = msr.iloc[i-1]['VD0'] == msr.iloc[i]['VD0'] and msr.iloc[i-1]['VD1'] == msr.iloc[i]['VD1']
            # matches next record?
            dupH = msr.iloc[i]['VD0'] == msr.iloc[i+1]['VD0'] and msr.iloc[i]['VD1'] == msr.iloc[i+1]['VD1']
            # assign AND of those to new column 'dup':
            msr.loc[msr.index[i], 'dup'] = True if dupL and dupH else False
  
        # return the non 'dup' rows, exluding the 'dup' column:
        return msr[msr['dup'] != True].loc[:, :'power1']

