from .colors import Colors
import config as config
#************************************************************
#                    The Message Class
#************************************************************

#This class is basicly just a prefab for messages that shall have a unique style.
class Msg:

    def warning(input):
        print(Colors.warning + input + Colors.reset)

    def error(input):
        print(Colors.error + input + Colors.reset)

    def debug(input):
        if(config.debug):
            print(Colors.fg.lightgrey + input + Colors.reset)

    def tcp(input):
        print(Colors.fg.lightcyan + input + Colors.reset)
        