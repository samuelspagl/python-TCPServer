from tcp.tcpListener import TcpListener
import config as config
import json

def main():

    while True:
        string = input("Please select a command (Type 'help' if you don't know the commands): \n--> ")
        cmd = string.split(" ")
        if cmd[0] == "start":
            tcp = TcpListener(config.ip_adress,config.port)
            tcp.connect()

        if cmd[0] == "startDev":
            tcp = TcpListener(config.dev_ip_adress, config.dev_port)
            tcp.connect()

        if cmd[0] == "stop":
            
            tcp.disconnect()

        if cmd[0] == "help":
            print("These are the aviable commands: \n- start: starts the server\n- startDev: starts the devServer\n- stop: stops the server")


if(__name__ == "__main__"):
    main()