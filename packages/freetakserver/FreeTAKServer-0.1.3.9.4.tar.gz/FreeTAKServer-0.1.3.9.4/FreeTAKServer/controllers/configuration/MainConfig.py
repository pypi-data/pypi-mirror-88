import os
currentPath = os.path.dirname(os.path.abspath(__file__))

class MainConfig:
    """
    this is the main configuration file and is the only one which
    should need to be changed
    """
    # this is the port to which clients will connect
    CoTServicePort = int(8087)

    # this needs to be changed for private data packages to work
    DataPackageServiceDefaultIP = str("0.0.0.0")

    # api port
    APIPort = 19023

    # api IP
    APIIP = '0.0.0.0'

    # allowed api's to access CLI commands
    AllowedCLIIPs = ['127.0.0.1']

    # whether or not to save CoT's to the DB
    SaveCoTToDB = bool(True)

    # this should be set before startup
    DBFilePath = str(r'/root/FTSDataBase.db')

    # the version information of the server (recommended to leave as default)
    version = 'FreeTAKServer-1.3 RC 2'

    ExCheckFilePath = str(r'/usr/local/lib/python3.6/dist-packages/FreeTAKServer/controllers/ExCheck/template')

    ExCheckChecklistFilePath = str(r'/usr/local/lib/python3.6/dist-packages/FreeTAKServer/controllers/ExCheck/checklist')

    # dict of API tokens and users should be changed
    # format of header should be {Authentication: Bearer 'TOKEN'}
    tokens = {
        "secret-token": "user"
    }

    nodeID = "FreeTAKServer-abc123"

    # set to None if you don't want a message sent
    ConnectionMessage = f'Welcome to FreeTAKServer {version}. The Parrot is not dead. It’s just resting'

    #keyDir = str(r"/usr/local/lib/python3.6/dist-packages/FreeTAKServer/Certs/ServerCerts/FTS.key")
    keyDir = r"/usr/local/lib/python3.6/dist-packages/FreeTAKServer/Certs/ServerCerts/server.key"

    #pemDir = str(r"/usr/local/lib/python3.6/dist-packages/FreeTAKServer/Certs/ServerCerts/FTS.pem")
    pemDir = r"/usr/local/lib/python3.6/dist-packages/FreeTAKServer/Certs/ServerCerts/server.pem" # or crt

    unencryptedKey = r"/usr/local/lib/python3.6/dist-packages/FreeTAKServer/Certs/ServerCerts/server.key.unencrypted"

    CA = r"/usr/local/lib/python3.6/dist-packages/FreeTAKServer/Certs/ServerCerts/ca.pem"

    password = str('atakatak')