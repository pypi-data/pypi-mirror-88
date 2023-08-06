import eventlet
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_httpauth import HTTPTokenAuth
import threading
from lxml import etree
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.RawCoT import RawCoT
from FreeTAKServer.controllers.ApplyFullJsonController import ApplyFullJsonController
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.model.ServiceObjects.FTS import FTS
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables as vars
from FreeTAKServer.model.SimpleClient import SimpleClient
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.configuration.DatabaseConfiguration import DatabaseConfiguration
from FreeTAKServer.controllers.RestMessageControllers.SendChatController import SendChatController
import os
import shutil
import json
from flask_cors import CORS
from FreeTAKServer.controllers.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController
from FreeTAKServer.controllers.RestMessageControllers.SendPresenceController import SendPresenceController
from FreeTAKServer.controllers.RestMessageControllers.SendEmergencyController import SendEmergencyController
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.controllers.JsonController import JsonController

dbController = DatabaseController()

UpdateArray = []

functionNames = vars()
functionNames.function_names()

jsonVars = vars()
jsonVars.json_vars()

restMethods = vars()
restMethods.rest_methods()

defaultValues = vars()
defaultValues.default_values()

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfiguration().DataBaseConnectionString
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
dbController.session = db.session
CORS(app)
socketio = SocketIO(app, async_handlers=True, async_mode="eventlet")
socketio.init_app(app, cors_allowed_origins="*")
APIPipe = None
CommandPipe = None
app.config["SECRET_KEY"] = 'vnkdjnfjknfl1232#'

@app.errorhandler(404)
def page_not_found(e):
    return 'this endpoint does not exist'

@auth.verify_token
def verify_token(token):
    output = dbController.query_APIUser(query=f'token == "{token}"')
    if output:
        return output[0].Username

@app.route('/')
def sessions():
    return b'working'

@socketio.on('connect')
def handle_message():
    emit('data', json.dumps({'abc234': 'test123'}))

@socketio.on('users')
def show_users():
    '''import random
    jsondata = {"Users":
                []}
    for user in range(random.randint(1, 100)):
        user = {"ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "callsign": f"{}"}
        jsondata["Users"].append(user)'''

@socketio.on('logs')

@socketio.on('serviceInfo')
def show_service_info():
    import random
    import datetime as dt
    DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
    timer = dt.datetime
    now = timer.utcnow()
    zulu = now.strftime(DATETIME_FMT)
    add = dt.timedelta(seconds=random.randint(60, 10000))
    stale_part = dt.datetime.strptime(zulu, DATETIME_FMT) - add
    starttime = stale_part.strftime(DATETIME_FMT)
    jsonObject = {
        "services": {
            "SSL_CoT_service": {
                          "status": random.choice(['on', 'off']),
                          "port": random.randint(1, 65535)
                      },
            "TCP_CoT_service": {
                          "status": random.choice(['on', 'off']),
                          "port": random.randint(1, 65535)
                      },
            "SSL_DataPackage_service": {
                          "status": random.choice(['on', 'off']),
                          "port": random.randint(1, 65535)
                      },
            "TCP_DataPackage_service": {
                          "status": random.choice(['on', 'off']),
                          "port": random.randint(1, 65535)
                      }
        },
        "starttime": str(starttime)
    }

    emit('serviceInfo', json.dumps(jsonObject))

@socketio.on("serverHealth")
def serverHealth():
    import random
    jsondata = {
                "CPU": random.randint(1, 100),
                "memory": random.randint(1, 100),
                "disk": random.randint(1, 100)
                }
    emit('serviceInfo', json.dumps(jsondata))

@app.route("/systemStatus", methods=["GET"])
def systemStatus():
    import random
    jsondata = {
        "services": {
            "SSL_CoT_service": {
                "status_expected": random.choice(['on', 'off']),
                "status_actual": random.choice(['on', 'off'])
            },
            "TCP_CoT_service": {
                "status_expected": random.choice(['on', 'off']),
                "satus_actual": random.choice(['on', 'off'])
            },
            "SSL_DataPackage_service": {
                "status_expected": random.choice(['on', 'off']),
                "status_actual": random.choice(['on', 'off'])
            },
            "TCP_DataPackage_service": {
                "status_expected": random.choice(['on', 'off']),
                "status_actual": random.choice(['on', 'off'])
            },
            "TCP_API_service": {
                "status_expected": random.choice(['on', 'off']),
                "status_actual": random.choice(['on', 'off'])
            }
        }
    }

@app.route("/SendGeoChat", methods=[restMethods.POST])
def SendGeoChat():
    try:
        json = request.json
        modelObject = Event.GeoChat()
        out = ApplyFullJsonController().serializeJsonToModel(modelObject, json)
        xml = XMLCoTController().serialize_model_to_CoT(out, 'event')
        from FreeTAKServer.controllers.SpecificCoTControllers.SendGeoChatController import SendGeoChatController
        rawcot = RawCoT()
        rawcot.xmlString = xml
        rawcot.clientInformation = None
        object = SendGeoChatController(rawcot)
        APIPipe.send(object.getObject())
        return '200', 200
    except Exception as e:
        print(e)



@app.route("/ManagePresence")
@auth.login_required()
def ManagePresence():
    pass

@app.route("/ManagePresence/postPresence", methods=[restMethods.POST])
@auth.login_required
def postPresence():
    try:
        from json import dumps
        #jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_presence_post(jsondata)
        Presence = SendPresenceController(jsonobj).getCoTObject()
        APIPipe.send(Presence)
        return Presence.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 500

@app.route("/ManageGeoObject")
@auth.login_required()
def ManageGeoObject():
    pass

@app.route("/ManageGeoObject/postGeoObject", methods=[restMethods.POST])
@auth.login_required
def postGeoObject():
    try:
        from json import dumps
        #jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'attitude': 'friend', 'geoObject': 'Ground', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_geoobject_post(jsondata)
        simpleCoTObject = SendSimpleCoTController(jsonobj).getCoTObject()
        APIPipe.send(simpleCoTObject)
        return simpleCoTObject.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 500

@app.route("/ManageChat")
@auth.login_required()
def ManageChat():
    pass

@app.route("/ManageChat/postChatToAll", methods=[restMethods.POST])
@auth.login_required
def postChatToAll():
    try:
        from json import dumps
        #jsondata = {'message': 'test abc', 'sender': 'natha'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_chat_post(jsondata)
        ChatObject = SendChatController(jsonobj).getCoTObject()
        APIPipe.send(ChatObject)
        return 'success', 200
    except Exception as e:
        return str(e), 500

@app.route("/ManageEmergency/getEmergency", methods=[restMethods.GET])
@auth.login_required
def getEmergency():
    try:
        from json import dumps
        output = dbController.query_ActiveEmergency()
        for i in range(0, len(output)):
            output[i] = output[i].__dict__
            del (output[i]['_sa_instance_state'])
        return jsonify(json_list=output), 200
    except Exception as e:
        return str(e), 200

@app.route("/ManageEmergency/postEmergency", methods=[restMethods.POST])
@auth.login_required
def postEmergency():
    try:
        from json import dumps

        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_emergency_post(jsondata)
        EmergencyObject = SendEmergencyController(jsonobj).getCoTObject()
        APIPipe.send(EmergencyObject)
        return EmergencyObject.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 200

@app.route("/ManageEmergency/deleteEmergency", methods=[restMethods.DELETE])
@auth.login_required
def deleteEmergency():
    try:
        from json import dumps
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_emergency_delete(jsondata)
        EmergencyObject = SendEmergencyController(jsonobj).getCoTObject()
        APIPipe.send(EmergencyObject)
        return 'success', 200
    except Exception as e:
        return str(e), 500

@app.route("/ManageEmergency")
@auth.login_required
def Emergency():
    pass

#@app.route("/ConnectionMessage", methods=[restMethods.POST])
def ConnectionMessage():

    try:
        json = request.json
        modelObject = Event.GeoChat()
        out = ApplyFullJsonController().serializeJsonToModel(modelObject, json)
        xml = XMLCoTController().serialize_model_to_CoT(out, 'event')
        from FreeTAKServer.controllers import SendGeoChatController
        rawcot = RawCoT()
        rawcot.xmlString = xml
        rawcot.clientInformation = None
        object = SendGeoChatController(rawcot).getObject()
        object.type = "connmessage"
        APIPipe.send(object.SendGeoChat)
        return '200', 200
    except Exception as e:
        print(e)

@app.route("/APIUser", methods=[restMethods.GET, restMethods.POST, restMethods.DELETE])
def APIUser():
    if request.remote_addr in MainConfig.AllowedCLIIPs:
        try:
            if request.method == restMethods.POST:
                json = request.get_json()
                dbController.create_APIUser(Username = json['username'], Token = json['token'])
                return 'success', 200

            elif request.method == restMethods.DELETE:
                json = request.get_json()
                username = json['username']
                dbController.remove_APIUser(query=f'Username == "{username}"')
                return 'success', 200

            elif request.method == restMethods.GET:
                output = dbController.query_APIUser()
                for i in range(0, len(output)):
                    output[i] = output[i].__dict__
                    del (output[i]['_sa_instance_state'])
                    del (output[i]['PrimaryKey'])
                    del (output[i]['uid'])
                return jsonify(json_list = output), 200

        except Exception as e:
            return str(e), 500
    else:
        return 'endpoint can only be accessed by approved IPs', 401
@app.route("/RecentCoT", methods=[restMethods.GET])
def RecentCoT():
    import time
    time.sleep(10)
    return b'1234'

@app.route("/URL", methods=[restMethods.GET])
def URLGET():
    data = request.args
    print(data)
    return 'completed', 200

@app.route("/Clients", methods=[restMethods.GET])
def Clients():
    try:
        if request.remote_addr in MainConfig.AllowedCLIIPs:
            CommandPipe.send([functionNames.Clients])
            out = CommandPipe.recv()
            returnValue = []
            for client in out:
                returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
            dumps = json.dumps(returnValue)
            return dumps
        else:
            return 'endpoint can only be accessed by approved IPs', 401
    except Exception as e:
        return str(e), 500

@app.route('/DataPackageTable', methods=[restMethods.GET, restMethods.POST, restMethods.DELETE])
def DataPackageTable():
    if request.remote_addr in MainConfig.AllowedCLIIPs:
        if request.method == "GET":
            output = dbController.query_datapackage()
            for i in range(0, len(output)):
                output[i] = output[i].__dict__
                del(output[i]['_sa_instance_state'])
                del(output[i]['CreatorUid'])
                del(output[i]['Hash'])
                del(output[i]['MIMEType'])
                del(output[i]['uid'])
            return jsonify(json_list = output), 200

        elif request.method == "DELETE":
            Hash = request.args.get('Hash')
            obj = dbController.query_datapackage(f'PrimaryKey == "{Hash}"')
            dbController.remove_datapackage(f'PrimaryKey == "{Hash}"')
            # TODO: make this coherent with constants
            currentPath = os.path.dirname(os.path.realpath(__file__))
            shutil.rmtree(f'{str(currentPath)}/FreeTAKServerDataPackageFolder/{obj[0].Hash}')
            return '200', 200
    else:
        return 'endpoint can only be accessed by approved IPs', 401

def getMission():
    import uuid
    import random_word
    import random
    maincontent = {
        "name": str(random_word.RandomWords().get_random_word()),
        "description": str(' '.join(random_word.RandomWords().get_random_words(limit=4))),
        "chatRoom": "",
        "tool": "public",
        "keywords": random_word.RandomWords().get_random_words(limit=random.randint(1, 3)),
        "creatorUid": str(random_word.RandomWords().get_random_word()),
        "createTime": "2020-12-09T15:53:42.873Z",
        "groups": random_word.RandomWords().get_random_words(limit=random.randint(1, 3)),
        "externalData": [],
        "uids": [{
            "data": str(uuid.uuid4()),
            "timestamp": "2020-12-09T15:58:10.635Z",
            "creatorUid": str(uuid.uuid4()),
            "details": {
                "type": "a-h-G",
                "callsign": "R.9.155734",
                "iconsetPath": "COT_MAPPING_2525B/a-h/a-h-G"
            }
        }
        ],
        "contents": [{
            "data": {
                "filename": str(random_word.RandomWords().get_random_word()),
                "keywords": [],
                "mimeType": "application/octet-stream",
                "name": str(' '.join(random_word.RandomWords().get_random_words(limit=random.randint(1, 2)))),
                "submissionTime": "2020-12-09T15:55:21.468Z",
                "submitter": str(random_word.RandomWords().get_random_word()),
                "uid": str(uuid.uuid4()),
                "hash": str(random.getrandbits(128)),
                "size": random.randint(1000, 100000)
            },
            "timestamp": "2020-12-09T15:55:21.559Z",
            "creatorUid": str(random_word.RandomWords().get_random_word())
        }
        ],
        "passwordProtected": random.choice(['true', 'false'])
    }
    return maincontent
@app.route("/missionTable", methods=['GET'])
def mission_table():
    try:
        import random

        jsondata = {
            "version": "3",
            "type": "Mission",
            "data": [getMission() for x in range(random.randint(1, 5))],
            "nodeId": "6ff99444fa124679a3943ee90308a44c9d794c02-e5a5-42b5-b4c8-625203ea1287"
        }
        return json.dumps(jsondata)
    except Exception as e:
        return e, 500

@app.route("/excheckTable", methods=["GET"])
def excheck_table():
    try:
        from FreeTAKServer.controllers.ExCheckControllers.templateToJsonSerializer import templateSerializer
        jsondata = templateSerializer().convert_object_to_json(DatabaseController().query_ExCheck())
        1 == 1
    except Exception as e:
        return str(e), 500
@app.route('/checkStatus', methods=[restMethods.GET])
def check_status():
    try:
        if request.remote_addr in MainConfig.AllowedCLIIPs:
            CommandPipe.send([functionNames.checkStatus])
            FTSServerStatusObject = CommandPipe.recv()
            out = ApplyFullJsonController().serialize_model_to_json(FTSServerStatusObject)
            return json.dumps(out), 200
        else:
            return 'endpoint can only be accessed by approved IPs', 401
    except Exception as e:
        return str(e), 500

@app.route('/changeStatus', methods=[restMethods.POST])
def All():
    try:
        if request.remote_addr in MainConfig.AllowedCLIIPs:
            FTSObject = FTS()
            if request.method == restMethods.POST:
                json = request.json
                if jsonVars.COTSERVICE in json:
                    CoTService = json[jsonVars.COTSERVICE]
                    FTSObject.CoTService.CoTServiceIP = CoTService.get(jsonVars.IP)
                    try:
                        FTSObject.CoTService.CoTServicePort = int(CoTService.get(jsonVars.PORT))
                    except:
                        FTSObject.CoTService.CoTServicePort = ''
                    FTSObject.CoTService.CoTServiceStatus = CoTService.get(jsonVars.STATUS)
                else:
                    pass
                if jsonVars.DATAPACKAGESERVICE in json:

                    DPService = json.get(jsonVars.DATAPACKAGESERVICE)
                    FTSObject.TCPDataPackageService.TCPDataPackageServiceIP = DPService.get(jsonVars.IP)
                    try:
                        FTSObject.TCPDataPackageService.TCPDataPackageServicePort = int(DPService.get(jsonVars.PORT))
                    except:
                        FTSObject.TCPDataPackageService.TCPDataPackageServicePort = ''
                    FTSObject.TCPDataPackageService.TCPDataPackageServiceStatus = DPService.get(jsonVars.STATUS)

                else:
                    pass

                if jsonVars.SSLCOTSERVICE in json:

                    SSLCoTservice = json[jsonVars.SSLCOTSERVICE]
                    FTSObject.SSLCoTService.SSLCoTServiceIP = SSLCoTservice.get(jsonVars.IP)
                    try:
                        FTSObject.SSLCoTService.SSLCoTServicePort = int(SSLCoTservice.get(jsonVars.PORT))
                    except:
                        FTSObject.SSLCoTService.SSLCoTServicePort = ''
                    FTSObject.SSLCoTService.SSLCoTServiceStatus = SSLCoTservice.get(jsonVars.STATUS)

                else:
                    pass

                CommandPipe.send([functionNames.Status, FTSObject])
                out = CommandPipe.recv()
                return '200', 200
        else:
            return 'endpoint can only be accessed by approved IPs', 401
    except Exception as e:
        return '500', 500

def receiveUpdates():
    while True:
        try:
            update = APIPipe.recv()
            global UpdateArray
            emitUpdates(update)
        except Exception as e:
            print(e)

def submitData(dataRaw):
    global APIPipe
    print(APIPipe)
    data = RawCoT()
    data.clientInformation = "SERVER"
    data.xmlString = dataRaw.encode()
    APIPipe.send([data])

def emitUpdates(Updates):
    data = [SimpleClient()]
    data[0].callsign = ''
    data[0].team = ''
    data[0].ip = ''
    returnValue = []
    for client in data:
        returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
    socketio.emit('up', json.dumps(returnValue), broadcast = True)
    data = Updates
    for client in data:
        returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
    socketio.emit('up', json.dumps(returnValue), broadcast = True)
    return 1

def test(json):
    modelObject = Event.dropPoint()
    out = XMLCoTController().serialize_CoT_to_model(modelObject, etree.fromstring(json))
    xml = XMLCoTController().serialize_model_to_CoT(out, 'event')
    from FreeTAKServer.controllers.SpecificCoTControllers.SendDropPointController import SendDropPointController
    rawcot = RawCoT()
    rawcot.xmlString = xml
    rawcot.clientInformation = None
    object = SendDropPointController(rawcot)
    print(etree.tostring(object.sendDropPoint.xmlString,pretty_print=True).decode())
    '''EventObject = json
    modelObject = ApplyFullJsonController(json, 'Point', modelObject).determine_function()
    out = XMLCoTController().serialize_model_to_CoT(modelObject, 'event')
    print(etree.tostring(out))
    print(RestAPI().serializeJsonToModel(modelObject, EventObject))'''



class RestAPI:
    def __init__(self):
        pass

    def startup(self, APIPipea, CommandPipea, IP, Port):
        global APIPipe, CommandPipe
        APIPipe = APIPipea
        CommandPipe = CommandPipea
        threading.Thread(target=receiveUpdates, daemon=True, args=()).start()
        socketio.run(app, host=IP, port=Port)
        # try below if something breaks
        # socketio.run(app, host='0.0.0.0', port=10984, debug=True, use_reloader=False)


    def serializeJsonToModel(self, model, Json):
        for key, value in Json.items():
            if isinstance(value, dict):
                submodel = getattr(model, key)
                out = self.serializeJsonToModel(submodel, value)
                setattr(model, key, out)
            else:
                setattr(model, key, value)
        return model

if __name__ == '__main__':
    excheck_table()
    #    app.run(host="127.0.0.1", port=80)

