from .actionTemplate import action
class Message(action):
    id = "MESSAGE"
    def run(data):
        msgString = data.decode('utf-8')
        print("The message is:\n" + msgString)