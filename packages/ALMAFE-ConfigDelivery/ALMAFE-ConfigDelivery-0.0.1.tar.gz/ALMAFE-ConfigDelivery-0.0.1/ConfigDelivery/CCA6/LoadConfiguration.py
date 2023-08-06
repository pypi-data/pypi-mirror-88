import configparser

def loadConfiguration():
    '''
    load our configuration file
    '''
    config = configparser.ConfigParser()
    config.read("ConfigDelivery.ini")
    host = config['CCA6Database']['host']
    database = config['CCA6Database']['database']
    user = config['CCA6Database']['user']
    passwd = config['CCA6Database']['passwd']
    filesroot = config['CCA6Files']['filesroot']
    return {'host' : host, 'database' : database, 'user' : user, 'passwd' : passwd, 'filesroot' : filesroot }
