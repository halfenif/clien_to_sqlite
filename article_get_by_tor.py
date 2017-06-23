import sys
import io
import pycurl
import stem.process
from stem.util import term
from itertools import count

import time
import socket
import os
import const_config

def get_socket_port():
    SOCKS_PORT = const_config.get_start_port()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)                     #2 Second Timeout

    print('Check Socket port:', SOCKS_PORT)
    for i in count(1):
        try:
            sock.bind(('127.0.0.1',SOCKS_PORT))
        except:
            print(i, 'Used Port No:', SOCKS_PORT)
            SOCKS_PORT += 1
        else:
            print(i, 'OK! SOCKS_PORT:', SOCKS_PORT)
            return SOCKS_PORT



#-------------------------------------------------------------------------------
# Create
def get_tor_process():
    print('-------------------------------------------------------------------')
    socket_port = get_socket_port()
    strDataFolder = const_config.get_temp_cache_folder() + str(socket_port)
    try:
        os.stat(strDataFolder)
    except:
        os.makedirs(strDataFolder)

    tor_process = stem.process.launch_tor_with_config(
        config = {
            #'tor_cmd':"C:/Users/junye/Desktop/Tor Browser/Browser/TorBrowser/Tor/Tor.exe",
            'SocksPort':str(socket_port),
            'DataDirectory':strDataFolder,
            #'Log': ['DEBUG stdout', 'ERR stderr' ],
            #'ExitNodes':'{ru}',
        },
        init_msg_handler = print_bootstarp_lines,
        timeout = 90,
    )

    return tor_process, socket_port

#-------------------------------------------------------------------------------
# BootStrap
def print_bootstarp_lines(line):
    #print("line:" + line)
    if "Bootstrapped" in line:
        #print(term.format(line, term.Color.BLUE))
        print(line)
        pass

#-------------------------------------------------------------------------------
# Kill
def kill_tor_process(tor_process):
    tor_process.kill()
    print('Tor Process Killed')

#-------------------------------------------------------------------------------
# Call
def get_article(url, socket_port):
    #print('article_get_by_tor.get_article()')
    time_start = time.time()

    out_return = '' #Init Value
    status_code = ''

    out_io = io.BytesIO()
    query = pycurl.Curl()
    query.setopt(pycurl.URL, url)
    query.setopt(pycurl.PROXY, 'localhost')
    query.setopt(pycurl.PROXYPORT, socket_port)
    query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
    query.setopt(pycurl.WRITEFUNCTION, out_io.write)

    query.perform()
    status_code = str(query.getinfo(pycurl.HTTP_CODE))
    if status_code == '200':
        out_return = out_io.getvalue().decode('utf-8','ignore')
                #  [ 7000 ][ 200 ][ 5sec ]
                #  [ 2017-06-10 09:06:05 ]
    seq = url.replace(const_config.get_baseurl(),'').replace(const_config.get_bbs_class()+'/','')
    print("[ {} ]                       [ {} ][ {}sec ][ {} ][ {} ][ {} ]".format(time.strftime('%x %X', time.localtime()), seq, round(time.time() - time_start), status_code, socket_port, const_config.get_bbs_class()  ))
    return status_code, out_return






#---------------------------------
# Main
if __name__ == "__main__":
    socket_port = get_socket_port()
    #print(term.format("Starting Tor:\n", term.Attr.BOLD))
    #print("Starting Tor:")
    url = "https://www.atagar.com/echo.php"
    url = "https://www.google.com"
    #url = "https://www.clien.net/service/board/park/10843228"
    # while(True):
    #     tor_process(url, socket_port)



    #print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
    #print("Checking our endpoint:")
