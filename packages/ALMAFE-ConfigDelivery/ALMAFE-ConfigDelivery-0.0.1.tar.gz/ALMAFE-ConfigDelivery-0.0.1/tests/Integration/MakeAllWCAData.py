from ConfigDelivery.WCA.WCADatabase import WCADatabase
import os
import glob

def deleteAllFiles(directory):
    files = glob.glob(os.path.join(directory, '*'))
    for f in files:
        os.remove(f)

def makeWCAData(band, showProgress = False):
    try:
        makeWCAData.db
    except:
        makeWCAData.db = WCADatabase()
    if showProgress:
        print("Band {0}:".format(band))
    directory = "SampleData_local\WCA{0}".format(band)
    deleteAllFiles(directory)
    makeWCAData.db.writeXML(directory, band, showProgress = showProgress, makePlot = band in (7, 8, 9))
        
def makeAllWCAData(showProgress = False):
    for band in (1, 3, 4, 5, 6, 7, 8, 9, 10):
        makeWCAData(band, showProgress)
