import const_config
import socket
from time import sleep
from itertools import count
from sys import exc_info

def check_socket_port():
    SOCKS_PORT = const_config.get_start_port()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)                     #2 Second Timeout

    print('Check Socket port:', SOCKS_PORT)
    for i in count(1):
        try:
            sock.bind(('127.0.0.1',SOCKS_PORT))
            sock.close()
            print(i, 'OK! SOCKS_PORT:', SOCKS_PORT)
        except:
            print("{} Useded Port No:{} {}".format(i, SOCKS_PORT, exc_info()[0]))


        SOCKS_PORT += 1
        sleep(1)

#---------------------------------
# Main
if __name__ == "__main__":
    check_socket_port()
