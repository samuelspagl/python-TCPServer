from lib.messages.colors import Colors
from lib.globalVars import GlobalVariables

class Msg:

    def warning(input):
        print(Colors.warning + input + Colors.reset)

    def error(input):
        print(Colors.error + input + Colors.reset)

    def debug(input):
        if(GlobalVariables.debug):
            print(Colors.fg.lightgrey + input + Colors.reset)

    def tcp(input):
        print(Colors.fg.lightcyan + input + Colors.reset)
        