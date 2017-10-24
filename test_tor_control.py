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


def test():
    control_port = 7000
    with Controller.from_port(port = control_port) as controller:
      controller.authenticate()

      print('---------------------------------------------------------')
      for circ in sorted(controller.get_circuits()):
        if circ.status != CircStatus.BUILT:
          continue

        print("")
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
    control_port = 7000
    try:
        controller = Controller.from_port(address='127.0.0.1', port=control_port)
    except stem.SocketError as exc:
        print("Unable to connect to tor on port 9051: %s" % exc)
        sys.exit(1)

    try:
        controller.authenticate()
    except stem.connection.MissingPassword:
        pw = getpass.getpass("Controller password: ")

        try:
            controller.authenticate(password = pw)
        except stem.connection.PasswordAuthFailed:
            print("Unable to authenticate, password is incorrect")
            sys.exit(1)
        except stem.connection.AuthenticationFailure as exc:
            print("Unable to authenticate: %s" % exc)
            sys.exit(1)

    #print("get_version",controller.get_version())
    #print("get_protocolinfo",controller.get_protocolinfo())
    #print("get_pid",controller.get_pid())
    #print("is_user_traffic_allowed",controller.is_user_traffic_allowed())
    #print("get_microdescriptor",controller.get_microdescriptor())
    #print("get_microdescriptors",controller.get_microdescriptors())
    #print("get_server_descriptor",controller.get_server_descriptor())
    #print("get_server_descriptors",controller.get_server_descriptors())
    #print("get_network_status",controller.get_network_status())

    #print("get_user",controller.get_user())
    #print("get_exit_policy",controller.get_exit_policy())
    #print("get_ports",controller.get_ports(stem.control.Listener))

    controller.signal(stem.Signal.DUMP )
    controller.close()
