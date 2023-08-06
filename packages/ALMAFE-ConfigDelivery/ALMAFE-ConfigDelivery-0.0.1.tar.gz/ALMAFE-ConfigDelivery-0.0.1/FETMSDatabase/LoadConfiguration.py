import configparser

def loadConfiguration():
    '''
    load our configuration file
    '''
    config = configparser.ConfigParser()
    config.read("ConfigDelivery.ini")
    host = config['FETMSDatabase']['host']
    database = config['FETMSDatabase']['database']
    user = config['FETMSDatabase']['user']
    passwd = config['FETMSDatabase']['passwd']
    return {'host' : host, 'database' : database, 'user' : user, 'passwd' : passwd}
