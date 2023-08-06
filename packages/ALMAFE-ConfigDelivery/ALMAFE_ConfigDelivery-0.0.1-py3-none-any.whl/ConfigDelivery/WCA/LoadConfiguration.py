import configparser

def loadConfiguration():
    '''
    load our configuration file
    '''
    config = configparser.ConfigParser()
    config.read("ConfigDelivery.ini")
    host = config['WCADatabase']['host']
    database = config['WCADatabase']['database']
    user = config['WCADatabase']['user']
    passwd = config['WCADatabase']['passwd']
    return {'host' : host, 'database' : database, 'user' : user, 'passwd' : passwd}
