from .actionTemplate import action
import os
import config as config

#************************************************************
#                    The Action Class
#************************************************************
class FileTransfer(action):
    #--------- THE ACTION ID ---------
    id = "FILE"
    #--------- THE RUN FUNCTION ------
    # The data frame is composed as followed
    # [4 byte INT]  [FILENAME]  [FILESIZE]  [FILEDATA]
    def run(data):
        flNameLen   = int.from_bytes(data[:4], 'little')    #FILE NAME SIZE
        data        = data[4:]                              
        flName      = data[:flNameLen].decode('utf-8')      #FILE NAME
        data        = data[flNameLen:]      
        flSize      = int.from_bytes(data[:4],'little')     #FILE SIZE
        data        = data[4:]
        
        filePath    = config.rec_folder + flName            #FILE DATA PATH

        try:
            file        = open(filePath,'wb')                   #creating the file
        except:
            os.mkdir(config.rec_folder)
            file        = open(filePath, 'wb')
        file.write(data)                            

        print("The file: " + flName + " has been created.")
        