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
import re
from urllib.parse import urljoin
from urllib.parse import urlparse

def get_socket_port():
    SOCKS_PORT = const_config.get_start_port()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)                     #2 Second Timeout

    print('[ {} ]                       [ Check Socket port ][ {} ]'.format(time.strftime('%x %X', time.localtime()), SOCKS_PORT))
    for i in count(1):
        try:
            sock.bind(('127.0.0.1',SOCKS_PORT))
        except:
            print('[ {} ]                       [ Used Port No ][ {} ]'.format(time.strftime('%x %X', time.localtime()), SOCKS_PORT))
            SOCKS_PORT += 1
        else:
            print('[ {} ]                       [ OK! SOCKS_PORT ][ {} ]'.format(time.strftime('%x %X', time.localtime()), SOCKS_PORT))
            return SOCKS_PORT


#-------------------------------------------------------------------------------
# Create
def get_tor_process(socket_port=0):
    # print('-------------------------------------------------------------------')
    if socket_port == 0:
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

    # print('Type of Tor Process:', type(tor_process))
    # print('PID of Tor Process:', tor_process.pid)

    return tor_process, socket_port

#-------------------------------------------------------------------------------
# BootStrap
def print_bootstarp_lines(line):
    #print("line:" + line)
    #Jul 10 19:31:06.000 [notice] Bootstrapped 90%: Establishing a Tor circuit
    if "Bootstrapped" in line:
        #print(term.format(line, term.Color.BLUE))
        idx = line.index("Bootstrapped")
        #print(line)
        print("[ {} ]                       [ {} ]".format(time.strftime('%x %X', time.localtime()), line[idx:]))

#-------------------------------------------------------------------------------
# Kill
def kill_tor_process(tor_process):
    tor_process.kill()
    print('Tor Process Killed')

#-------------------------------------------------------------------------------
# Call
def get_article(url, socket_port, seq=0):
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

    url_path_split = [x for x in re.sub(r':?service|board','',urlparse(url).path).split('/') if x]
    bbsclass = url_path_split[0]
    # print("[ {} ]                       [ {} ][ {} ][ {} ][ {}sec ][ {} ]".format(time.strftime('%x %X', time.localtime()),
    #                                                                               socket_port,
    #                                                                               format(int(seq),','),
    #                                                                               status_code,
    #                                                                               round(time.time() - time_start),
    #                                                                               bbsclass
    #                                                                               ))
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
