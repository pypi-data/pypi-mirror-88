from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
import os.path
import csv
import glob
import re
import tempfile
import zipfile

class WCADataFiles(object):
    '''
    Class for accessing WCA raw measurment data on CVFiler
    '''
    DATA_FILES_ROOT = r"\\cvfiler\LO\ALMA Documentation NEW"
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def openWCADataPackage(self, band, serialNum, showProgress = False):
        # metadata for found file will go here: 
        item = None
        # make the WCA's root path:
        path = r"{:s}\Band_{:d}\WCA\SN{:03d}\Test Data".format(self.DATA_FILES_ROOT, band, serialNum)
        if os.path.exists(path):
            # look here for the 'WCAs.CSV' file:
            item = self.findCSV(path, showProgress = showProgress)
            # if item is True but not a dict, we will skip looking in zip files.
            if not item:
                # not found.  look for ZIP files...
                pattern = os.path.join(path, "*.zip")
                files = glob.glob(pattern)
                if files:
                    toOpen = None
                    maxRMA = 0
                    if len(files) == 1:
                        # just one found:
                        path = files[0]
                        toOpen = path
                    else:
                        # loop to find the highest RMA zip file:
                        for path in files:
                            if showProgress:
                                print(path)
                            file = os.path.basename(path)
                            # find RMA<int> in name, with or without space between:
                            RMA = re.findall(r"RMA\s*\d+", file)
                            if RMA:
                                # make int removing 'RMA' and stripping any spaces:
                                RMA = int(RMA[0][3:].strip())                                        
                                if RMA > maxRMA:
                                    # newer than previously seen
                                    maxRMA = RMA
                                    toOpen = path
                            elif not toOpen:
                                # it might be something like "Production Test Data.." in which case we'll use it if no 'RMA':
                                Production = re.findall("Production", file)
                                if Production:
                                    toOpen = path
                    if toOpen:
                        if showProgress:
                            print("opening {0}".format(toOpen))
                        # make a local temp directory to unzip into:
                        unzipTo = tempfile.TemporaryDirectory(prefix="WCADB")
                        with zipfile.ZipFile(toOpen, 'r') as zip_ref:
                            zip_ref.extractall(unzipTo.name)
                        # search for the 'WCAs.CSV' file there:
                        item = self.findCSV(unzipTo.name, showProgress = showProgress)
                        if not item:
                            # not found; look for subdirectories:
                            pattern = os.path.join(unzipTo.name, "*Data*")
                            files = glob.glob(pattern)
                            if files:
                                # if found, search the first subdirectory:
                                item = self.findCSV(files[0], showProgress = showProgress)
                        # save the reference to the temp directory so it doesn't get deleted yet:
                        if item:
                            item['unzipTo'] = unzipTo
                        

        # if found and it is a dict:
        if (item):
            # don't trust the file's serialNum over our own:
            item['serialNum'] = serialNum
        return item
    
    def readWCACSV(self, band = None, serialNum = None, showProgress = False):
        '''
        Read one or more 'WCAs.CSV' metadata files from CVFiler
        :param band:int if provided, filter by band (1..10)
        :param serialNum:str if provided find the record for a specific unit. Only has effect if band is provided.
        :param showProgress: if True, print file names loaded
        :return list of dict{band, serialNum, timeStamp, ESN, fLoYig, fHiYig, VG0, VG1}
        '''
        if not band:
            # search all bands except band 2:
            bands = [1, 3, 4, 5, 6, 7, 8, 9, 10]
        else:
            # search the specified band:
            bands = [band] 
        
        if not serialNum:
            # search all serialNums:
            serialNums = [n for n in range(1, 99)]
        else:
            # search the specified serialNum:
            serialNums = [int(serialNum)]
        
        output = []
        
        # loop over the specified band+serialNum combinations:
        for band in bands:
            for serialNum in serialNums:
                # ignore pre-production band 5 units:
                if band == 5 and serialNum >= 10:
                    # metadata for found file will go here: 
                    item = self.openWCADataPackage(band, serialNum, showProgress = showProgress)
                    # if found and it is a dict:
                    if (item and not item is True):
                        output.append(item)                        
        return output
    
    def findCSV(self, path, showProgress = False):
        '''
        Search a directory for the 'WCAs.CSV' metadata file from CVFiler
        If found, read it and return its contents.
        :param path: directory to search
        :param showProgress: if true and found, print the found path/filename
        :return None if not found
                dict{path, band, serialNum, timeStamp, ESN, fLoYig, fHiYig, VG0, VG1} if found and parsed
        '''
        pattern = os.path.join(path, "*WCAs*.csv")
        files = glob.glob(pattern)
        if files:
            path = files[0]
            found = self.readOneCSV(path)
            if showProgress and found:
                print("found {}".format(os.path.basename(path)))
            return found
        return None
    
    def readOneCSV(self, path):
        '''
        Read a single 'WCAs.CSV' metadata file from CVFiler
        :param path: the file to read
        :return dict{path, band, serialNum, timeStamp, ESN, fLoYig, fHiYig} or None
                may have items VG0, VG1 if found
        '''
        output = None
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if not output:
                    try:
                        output = {'path' : path,
                                  'band' : row[0],
                                  'serialNum' : row[1],
                                  'timeStamp' : makeTimeStamp(row[2]),
                                  'ESN' : row[5],
                                  'fLoYig' : row[6],
                                  'fHiYig' : row[7]
                                 }
                    except:
                        pass
                    try:
                        if output:
                            output['VG0'] = row[13]
                            output['VG1'] = row[14]
                    except:
                        if output:
                            output['VG0'] = None
                            output['VG1'] = None
                        pass
        return output
    
    def readOutputPower(self, band, serialNum, showProgress = False):
        item = self.openWCADataPackage(band, serialNum, showProgress)
        if item:
            path = os.path.dirname(item['path'])
            pattern = os.path.join(path, "*WCA_OUTPUT_POWER*.csv")
            files = glob.glob(pattern)
            if files:
                if showProgress:
                    print("found {}".format(os.path.basename(files[0])))
                return (files[0], self.readOneOutputPower(files[0], item['VG0'], item['VG1']))
            else:
                return (None, None)
    
    def readOneOutputPower(self, path, VG0 = None, VG1 = None):
        output = []
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if len(row) == 1:
                    if not VG0:
                        # ! Pol0 : VG (V) set: -0.450
                        found = re.search(r"Pol0.*VG.*[+=]?(\d+(\.\d*)?|\.\d+)", row[0])
                        if found:
                            VG0 = float(found[0][-7:].strip())                                        
                    if not VG1:
                        # ! Pol1 : VG (V) set: -0.450                                    
                        found = re.search(r"Pol1.*VG.*[+=]?(\d+(\.\d*)?|\.\d+)", row[0])
                        if found:
                            VG1 = float(found[0][-7:].strip())
                try:
                    # ! keyBand keyDataSet fkWCA TS FreqLO Power PolOutput VD0 VD1 VG0 VG1
                    if len(row) >= 10:
                        try:
                            if not VG0:
                                VG0 = float(row[9])
                            if not VG1:
                                VG1 = float(row[10])
                        except:
                            pass
                        
                    output.append({'band' : int(row[0]),
                                   'dataSet' : int(row[1]),
                                   'serialNum' : int(row[2]),
                                   'timeStamp' : makeTimeStamp(row[3]),
                                   'freqLO' : float(row[4]),
                                   'power' : float(row[5]),
                                   'pol' : float(row[6]),
                                   'VD0' : float(row[7]),
                                   'VD1' : float(row[8]),
                                   'VG0' : VG0,
                                   'VG1' : VG1
                                  })
                except:
                    pass             
        return output
