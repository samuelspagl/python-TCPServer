import config as config
from .messages.msg import Msg
import socket
import threading
from .dataActions.dataTypes import *
from .dataActions.actionTemplate import action

class TcpListener: 
    
    #**********************************************
    #                 Constructor 
    #**********************************************
    def __init__ (self, ip_adress, port):
        self.ipAdress       = ip_adress
        self.port           = port
        self.server_adress  = (self.ipAdress, self.port)
        self.sock           = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.workerThread   = threading.Thread(target=self.listen, daemon=False)
        self.isActive       = False


    #**********************************************
    #                 Listen 
    #**********************************************

    def listen(self):
        self.isActive = True                
        self.sock.bind(self.server_adress)  #Binding the server to the Adress
        Msg.tcp("Starting a TCP Server on {0}:{1}".format(self.ipAdress, self.port))
        
        self.sock.listen(1)                                     #Start listening for 1 client, every other client will be denied
        while self.isActive:
            Msg.tcp("waiting for connection")
            connection, client_adress = self.sock.accept()      #Accepting the first connection

            while connection:
                Msg.tcp("Connection from {0}:{1}".format(client_adress[0],client_adress[1]))

                recData     = bytearray()                       #Array for cumulative data
                argsLen     = -1                                #var for argument length:   -1=none
                arg         = ""                                #var for argmument          ""=none
                dataSize    = -1                                #var for dataSize           -1=none

                while True:                                     #While there is a connection
                    data        = connection.recv(4096)         #recieve the data
                    recData     += data                         #add Data to the recData bytearray
                    moreData    = False
                    if not data:                                #if no data was transmitted
                        Msg.tcp("Connection closed")            
                        argsLen     = -1                        #reset all arguments
                        arg         = ""                        #<--
                        dataSize    = -1                        #<--
                        connection  = None                      #close the connection
                        break

                    #Receiving data structured like this:
                    #[4 byte Integer]   [arg in bytes]  [4 byte Integer]    [data]
                    #= length of Arg     =arg in bytes  = length of Data    = can contain more arguments, or just data
                    #
                    #--> This way the function can search in the classes data actions of the action with the ID=arg and run the function with all the data
                    
                    while moreData == False:                                    #as long as enough data is provided in the recData bytearray
                        #------- Argument Length -------
                        if (len(recData)>4) and (argsLen == -1):    
                            argsLen = int.from_bytes(recData[:4],'little')
                            recData = recData[4:]
                        else:
                            moreData = True                                         #check if more Data is needed
                        #------- Argument String -------
                        if (len(recData)>argsLen) and (arg == ''):  
                            arg     = recData[:argsLen].decode('utf-8')
                            recData = recData[argsLen:]
                        else:
                            moreData = True                                         #check if more Data is needed                         
                        #------- Data Frame Size -------
                        if (len(recData)>4) and (dataSize == -1):
                            dataSize    = int.from_bytes(recData[:4], 'little')
                            recData     = recData[4:]
                        else:
                            moreData = True                                         #check if more Data is needed
                        #-------        Data     -------
                        if (len(recData)>= dataSize):
                            dt          = recData[:dataSize]
                            recData     = recData[dataSize:]
                            actionFound = False                                     #check if an action with the name {arg} was found
                            for ac in acs:                                          #--> search in all actions
                                if ac.id == arg:                                    #--> if a action with the id = {arg} is found
                                    actionFound = True
                                    ac.run(dt)                                      #--> run the method from the action
                            if not actionFound:
                                Msg.error("The DataType is '" + arg + "' but no suitable action has been found. Please add one, if you want to ust this Type.")
                            argsLen     = -1                                        #reset all variables
                            arg         = ""                                        #<--
                            dataSize    = -1                                        #<--
                        else:
                            moreData = True
                        
                        if len(recData) == 0:                                       #if the recData bytearray is 0 wait for new Data
                            moreData = True
                        

                        
                        

    #**********************************************
    #               Connect Method 
    #**********************************************

    def connect(self):
        self.workerThread.start()

        

    #**********************************************
    #              Disconnect Method 
    #**********************************************
    def disconnect(self):
        self.isActive = False
        try:
            self.sock.close()
        except:
            None
        
        