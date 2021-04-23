from lib.tcp.tcpListener import TcpListener
import time as t

def main():
    print("Stuff")

    tcp = TcpListener()
    tcp.connect()
    t.sleep(3)


if(__name__ == "__main__"):
    main()