import sys
import os
import const_config
import argparse
from itertools import count
import time
from time import gmtime, strftime
import z_utils
import article_get
import article_parse
import db_article
import db_agent
import db_article_index
import article_get_by_tor

#---------------------------------
# Tor Process Loop
def tor_loop(args, callcount):
    tor_process = None
    #Init Agent
    item = {}
    item['agentid'] = args.socket_port

    #Make Target
    target = db_article_index.getTarget(item)

    if len(target) == 0:
        print('END: Target is Empty!!')
        print('Sleep 10 Min')
        sys.stdout.flush()
        time.sleep(600)
        return

    try:
        tor_process, socket_port = article_get_by_tor.get_tor_process(args.socket_port)
        item['agentid'] = socket_port
        item['processid'] = os.getpid()
        item['subprocessid'] = tor_process.pid
        item['countloop'] = callcount

        db_agent.initAgent(item)
        get_article(socket_port, target, args, callcount)
    except:
        print("tor_loop:{}".format(sys.exc_info()[0]))
        print("tor_loop:{}".format(sys.exc_info()[1]))
        print("tor_loop:{}".format(sys.exc_info()[2]))
    finally:
        db_agent.logAgent(item)
        if tor_process != None:
            article_get_by_tor.kill_tor_process(tor_process)

#---------------------------------
# Main Suit
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crawing User')
    parser.add_argument('-p', dest='socket_port', action='store', type=int,
                       default=0,
                       help='Socket Port for TOR')

    parser.add_argument('-f', dest='filewrite', action='store_true',
                       help='Request Out to Write File')

    #Parse Argument
    args = parser.parse_args()

    for callcount in count(0):
        try:
            tor_loop(args, callcount)
        except KeyboardInterrupt:
            print('KeyboardInterrupt. Cancled By Cntl+C')
            try:
                sys.exit(0)
            except:
                os._exit(0)
        except:
            print("__name__:{}".format(sys.exc_info()[0]))
            print("__name__:{}".format(sys.exc_info()[1]))
            print("__name__:{}".format(sys.exc_info()[2]))
            print('Sleep 30sec for socket End')
            time.sleep(30)
