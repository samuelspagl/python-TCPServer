from .actionTemplate import action

class Message(action):
    id = "MESSAGE"
    def run(data):
        print("doStuff")