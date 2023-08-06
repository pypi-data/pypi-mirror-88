import os
currentPath = os.path.dirname(os.path.abspath(__file__))
from pathlib import Path


class MainConfig:
    """
    this is the main configuration file and is the only one which
    should need to be changed
    """
    # this is the port to which clients will connect
    CoTServicePort = int(8087)

    SSLCoTServicePort = int(8089)

    # this needs to be changed for private data packages to work
    DataPackageServiceDefaultIP = str("0.0.0.0")

    python_version = 'python3.8'

    userpath = '/usr/local/lib/'

    # api port
    APIPort = 19023

    # api IP
    APIIP = '0.0.0.0'

    # allowed ip's to access CLI commands
    AllowedCLIIPs = ['127.0.0.1']

    # IP for CLI to access
    CLIIP = '127.0.0.1'

    # whether or not to save CoT's to the DB
    SaveCoTToDB = bool(True)

    # this should be set before startup
    DBFilePath = str(r'/root/FTSDataBase.db')

    # the version information of the server (recommended to leave as default)
    version = 'FreeTAKServer-1.3 RC 5'

    ExCheckMainPath = str(Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer/ExCheck'))

    ExCheckFilePath = str(Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer/ExCheck/template'))

    ExCheckChecklistFilePath = str(Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer/ExCheck/checklist'))

    DataPackageFilePath = str(Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer/FreeTAKServerDataPackageFolde'))

    # format of API message header should be {Authentication: Bearer 'TOKEN'}

    nodeID = "FreeTAKServer-abc123"

    # set to None if you don't want a message sent
    ConnectionMessage = f'Welcome to FreeTAKServer {version}. The Parrot is not dead. It’s just resting'

    #keyDir = str(r"/usr/local/lib/python3.6/dist-packages/FreeTAKServer/Certs/ServerCerts/FTS.key")
    keyDir = str(Path(rf"{userpath}{python_version}/dist-packages/FreeTAKServer/Certs/ServerCerts/pubserver.key"))

    #pemDir = str(r"/usr/local/lib/python3.6/dist-packages/FreeTAKServer/Certs/ServerCerts/FTS.pem")
    pemDir = str(Path(rf"{userpath}{python_version}/dist-packages/FreeTAKServer/Certs/ServerCerts/pubserver.pem")) # or crt

    unencryptedKey = str(Path(rf"{userpath}{python_version}/dist-packages/FreeTAKServer/Certs/ServerCerts/pubserver.key.unencrypted"))

    CA = str(Path(rf"{userpath}{python_version}/dist-packages/FreeTAKServer/Certs/ServerCerts/ca.pem"))

    password = str('atakatak')
