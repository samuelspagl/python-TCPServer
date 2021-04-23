from .actionTemplate import action

class FileTransfer(action):
    id = "FILETRANSFER"
    def run(data):
        print("doStuff")