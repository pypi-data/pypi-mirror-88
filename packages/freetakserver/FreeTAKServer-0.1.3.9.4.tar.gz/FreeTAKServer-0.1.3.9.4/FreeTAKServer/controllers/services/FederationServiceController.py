from multiprocessing import TimeoutError
from FreeTAKServer.controllers.FederatedCoTController import FederatedCoTController
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.protobufModel.fig_pb2 import FederatedEvent
import codecs
import socket
from FreeTAKServer.model.ServiceObjects.Federate import Federate

class FederationServiceController:
    def __init__(self, ip, port, connection):
        self.ip = ip
        self.port = port
        self.pool = None
        self.buffer = 4
        self.excessData = None
        self.killSwitch = False
        self.connection = connection


    def start(self):

        federateObject = Federate()
        federateObject.federationController = self
        federateObject.IP = self.connection.getpeername()[0]
        federateObject.Port = self.connection.getpeername()[1]
        federateObject.Socket = self.connection
        return federateObject

    def establish_connection(self, ip, port):
        # returns a socket object
        pass

    def disconnect(self):
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            return 1
        except:
            self.connection.close()
            return 1

    def generate_header(self, contentlength):
        tempHex = format(contentlength, 'x')
        if (len(tempHex) % 2) == 0:
            filteredhex = [(tempHex[i:i + 2]) for i in range(0, len(tempHex), 2)]
            while len(filteredhex) < 4:
                filteredhex.insert(0, '00')
            filteredhex = r'\x'.join(filteredhex)
            filteredhex = r'\x' + filteredhex
            filteredhex = codecs.escape_decode(filteredhex)[0]
            return filteredhex
        else:
            tempHex = '0'+tempHex
            filteredhex = [(tempHex[i:i + 2]) for i in range(0, len(tempHex), 2)]
            while len(filteredhex) < 4:
                filteredhex.insert(0, '00')
            filteredhex = r'\x'.join(filteredhex)
            filteredhex = r'\x' + filteredhex
            filteredhex = codecs.escape_decode(filteredhex)[0]
            return filteredhex

    def get_header_length(self, header):
        try:
            headerInHex = header.split(b'\\x')
            headerInHex = b''.join(headerInHex)
            return int(headerInHex, 16)
        except:
            return -1

    def receive_data_from_federates(self):
        # returns data received from federate
        # the following logic receives data from the federate and processes the protobuf
        # up to 100 CoT's
        dataCount = 0
        dataArray = []
        # 100 is the limit of data which can be received from a federate in one iteration
        while dataCount < 100:
            dataCount += 1
            try:
                try:
                    self.connection.settimeout(0.01)
                    data = self.connection.recv(self.buffer)
                    self.connection.settimeout(0)
                except TimeoutError:
                    break

                except Exception as e:
                    self.disconnect()
                    self.killSwitch = True
                    return 0
                if data != [b'']:
                    header = data[0]
                    content = self.connection.recv(self.get_header_length(header))
                    EmptyFTSObject = Event.FederatedCoT()
                    protoObject = FederatedEvent().FromString(content)
                    print(protoObject)
                    FTSObject = FederatedCoTController().serialize_main_contentv1(protoObject, EmptyFTSObject)
                    print('received data from Federate')
                    print(content)
                else:
                    self.killSwitch = True

                dataArray.append(FTSObject)

            except Exception as e:
                pass

    def send_data_to_federates(self, data):
        try:

            # sends supplied data to supplied socket upon being called
            federatedEvent = FederatedEvent()
            ProtoObj = FederatedCoTController().serialize_from_FTS_modelv1(federatedevent=federatedEvent, ftsobject=data)
            protostring = ProtoObj.SerializeToString()
            header = self.generate_header(len(protostring))
            protostring = header + protostring
            print(b'sent '+protostring+b' to federate')
            self.connection.send(protostring)
            return 1

        except Exception as e:
            pass

    def recv_in_data_pipe(self, pipe):
        pass

    def send_in_data_pipe(self, pipe, data):
        pass
