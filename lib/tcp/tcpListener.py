from lib.globalVars import GlobalVariables
from lib.messages.msg import Msg
import socket
import threading
from lib.dataActions.dataTypes import *
from lib.dataActions.actionTemplate import action

class TcpListener: 
    
    def __init__ (self):
        self.ipAdress       = GlobalVariables.ip_adress
        self.port           = GlobalVariables.port
        self.server_adress  = (self.ipAdress, self.port)
        self.sock           = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.workerThread   = threading.Thread(target=self.listen, daemon=True)
        self.isActive       = False

    def listen(self):
        self.isActive = True
        self.sock.bind(self.server_adress)
        Msg.tcp("Starting a TCP Server on {0}:{1}".format(self.ipAdress, self.port))
        
        self.sock.listen(1)
        while True:
            Msg.tcp("waiting for connection")
            connection, client_adress = self.sock.accept()

            while connection:
                Msg.tcp("Connection from {0}:{1}".format(client_adress[0],client_adress[1]))

                recData = bytearray()
                argsLen = -1
                arg = ""
                dataSize = -1

                while True:
                    data = connection.recv(4096)
                    recData += data
                    if not data:
                        Msg.tcp("Connection closed")
                        break

                    #Receiving data structured like this:
                    #[4 byte Integer]   [arg in bytes]  [4 byte Integer]    [data]
                    #= length of Arg     =arg in bytes  = length of Data    = can contain more arguments, or just data
                    #
                    #--> This way the function can search in the classes data actions of the action with the ID=arg and run the function with all the data

                    if (len(recData)>4) and (argsLen == -1):
                        argsLen = int.to_bytes(recData[:4],'little')
                        recData = recData[4:]
                    elif (len(recData)>argsLen) and (arg == ""):
                        arg = recData[:argsLen].decode('utf-8')
                        recData = recData[argsLen:]
                    elif (len(recData)>4) and (dataSize == -1):
                        dataSize = int.to_bytes(recData[:4], 'little')
                        recData = recData[4:]
                    elif (len(recData)>= dataSize):
                        dt = recData[:dataSize]
                        recData = recData[dataSize:]
                        actionFound = False
                        for ac in acs:
                            if ac.id == arg:
                                actionFound = True
                                ac.run(dt)
                        if not actionFound:
                            Msg.error("The DataType is '" + arg + "' but no suitable action has been found. Please add one, if you want to ust this Type.")

                            
                        #SEARCH FOR THE RIGHT FUNCTION

                        argsLen = -1
                        arg = ""
                        dataSize = -1
                        

    def connect(self):
        self.workerThread.start()

        
    def disconnect(self):
        self.sock.close()
        
        