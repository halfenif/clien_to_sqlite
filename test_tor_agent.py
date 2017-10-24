import sys
import io
import time
import socket
import os

import stem.process
from stem.util import term
from stem import Signal
from stem.control import Controller
from stem import CircStatus

import const_config

from itertools import count
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
# Create
def get_tor_process(socket_port):


    strDataFolder = const_config.get_temp_cache_folder() + str(socket_port)
    try:
        os.stat(strDataFolder)
    except:
        os.makedirs(strDataFolder)

    tor_process = stem.process.launch_tor_with_config(
        config = {
            #'tor_cmd':"C:/Users/junye/Desktop/Tor Browser/Browser/TorBrowser/Tor/Tor.exe",
            'ControlPort': str(7000),
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
# Kill
def kill_tor_process(tor_process):
    tor_process.kill()
    print('Tor Process Killed')


def tor_status():
    control_port = 7000
    with Controller.from_port(port = control_port) as controller:
      controller.authenticate()

      print('---------------------------------------------------------')
      for circ in sorted(controller.get_circuits()):
        if circ.status != CircStatus.BUILT:
          continue

        print("Circuit %s (%s)" % (circ.id, circ.purpose))

        for i, entry in enumerate(circ.path):
          div = '+' if (i == len(circ.path) - 1) else '|'
          fingerprint, nickname = entry

          desc = controller.get_network_status(fingerprint, None)
          address = desc.address if desc else 'unknown'

          print(" %s- %s (%s, %s)" % (div, fingerprint, nickname, address))

#---------------------------------
# Main
if __name__ == "__main__":
    try:
        tor_process = get_tor_process(7001)
        for callcount in count(0):
            print(callcount)
            tor_status()
            sys.stdout.flush()
            time.sleep(10)
    finally:
        kill_tor_process(tor_process)
