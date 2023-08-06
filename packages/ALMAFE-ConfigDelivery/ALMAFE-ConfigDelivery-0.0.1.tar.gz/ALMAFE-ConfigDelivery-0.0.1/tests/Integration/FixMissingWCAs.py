'''
Created on Nov 10, 2020

@author: mmcleod
'''
from ConfigDelivery.WCA.WCADatabase import WCADatabase
from ConfigDelivery.WCA.WCADataFiles import WCADataFiles
from ConfigDelivery.WCA.WCAOutputPower import WCAOutputPower


def findMissingWCAs(band = None, serialNum = None, showProgress = False, updateESN = False, updateYIG = False, updateVGs = False):
    db = WCADatabase()
    return db.verifyWCA(band, serialNum, showProgress = showProgress, updateESN = updateESN, updateYIG = updateYIG, updateVGs = updateVGs)

def findMissingPowerData(band = None, serialNum = None, showProgress = False):
    db = WCADatabase()
    configs = db.getWCAConfig(band, serialNum)
    output = []
    if not configs:
        return output
    for item in configs:
        found = False
        skip = False
        if not 4 <= item['band'] <= 10:
            skip = True
        try:
            # for numeric SN strings:
            SN = 'WCA{}-{:02d}'.format(item['band'], int(item['serialNum']))
            if item['band'] == 5 and int(item['serialNum']) < 10:
                skip = True
        except:
            skip = True

        if not skip:
            if showProgress:
                print(SN + " ", end='', flush=True)
            allRows = db.loadOutputPower(item['configId'])
            if allRows is None:
                pass
            elif allRows.empty:
                pass
            else:
                found = True
            if not found:
                output.append({'band' : item['band'],
                              'serialNum' : int(item['serialNum']),
                              'configId' : item['configId']
                             })
            if showProgress:
                if found:
                    print("OK")
                else:
                    print("not found")
    return output

def loadMissingOutputPower(band = None, serialNum = None, showProgress = False):
    db = WCAOutputPower()
    df = WCADataFiles()
    missing = findMissingPowerData(band, serialNum, showProgress = showProgress)
    for item in missing:
        path, rows = df.readOutputPower(item['band'], item['serialNum'], showProgress = showProgress)
        if path and rows:
            path = path.replace("\\", "\\\\")
            db.insertOutputPower(item['configId'], rows, r"loaded from {0}".format(path))
            if showProgress:
                print("loaded {0}".format(path))
            
            
