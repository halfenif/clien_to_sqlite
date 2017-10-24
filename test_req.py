import sys
import io
import time
import socket
import os

import requests
import re
from itertools import count
from urllib.parse import urljoin
from urllib.parse import urlparse

import const_config
import z_utils

import stem.process
from stem.util import term
from stem import Signal
from stem.control import Controller
from stem import CircStatus

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
            #'ControlPort': str(socket_port-1000),
            'SocksPort': str(socket_port),
            'DataDirectory': strDataFolder,
            #'Log': ['DEBUG stdout', 'ERR stderr' ],
            #'ExitNodes':'{ru}',
        },
        init_msg_handler = print_bootstarp_lines,
        timeout = 90,
    )

    #print('Type of Tor Process:', type(tor_process))
    #print('PID of Tor Process:', tor_process.pid)

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
        print("[ {} ]                       [ ---- ][ {} ]".format(time.strftime('%x %X', time.localtime()), line[idx:]))
        sys.stdout.flush()

#-------------------------------------------------------------------------------
# Kill
def kill_tor_process(tor_process):
    tor_process.kill()
    print('Tor Process Killed')

#-------------------------------------------------------------------------------
# Call
def get_article(url, socket_port, seq=0):
    time_start = time.time()

    out_return = '' #Init Value
    status_code = ''

    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:{socket_port}'.format(socket_port=socket_port),
                       'https': 'socks5://127.0.0.1:{socket_port}'.format(socket_port=socket_port)}

    session.headers.update({'Accept':'', 'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'})

    #response = requests.get(url, headers=headers, proxies=proxyDict)
    response = session.get(url)

    status_code = str(response.status_code)
    print('status_code', status_code)
    out_return = response.text
    z_utils.strToFile(out_return, 'request_test', 'html')
    return status_code, out_return

#---------------------------------
# Main
if __name__ == "__main__":
    url = "https://www.google.com"
    url = "https://www.clien.net/service/board/cm_vcoin/11257927"

    try:
        tor_process, socket_port = get_tor_process()
        get_article(url, socket_port)
    finally:
        kill_tor_process(tor_process)
