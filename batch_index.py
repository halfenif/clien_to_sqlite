import sys
import os
import argparse
import requests
import re
from itertools import count
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import const_config
import article_get_by_tor
import db_article_index
import db_agent
import z_utils
import time

def get_list(socket_port, args, callcount):
    countok = 0
    countfail = 0
    baseurl = ''

    if args.targetboard == 'board':
        baseurl = const_config.get_boardurl()
    elif args.targetboard == 'cm':
        baseurl = const_config.get_cmurl()



    page = args.startpage
    while 1:
        if countfail >= const_config.get_agent_reset_count():
            page = args.startpage
            countfail = 0
            print('-----------------------------------------------------------')
            print('Sleep 10 Min')
            sys.stdout.flush()
            time.sleep(600)

        url =  baseurl + '?po=' + str(page)
        if args.articlePeriod:
            url = url + '&articlePeriod=' + args.articlePeriod

        #print('url', url)
        status_code, resutl_context = article_get_by_tor.get_article(url, socket_port, page)

        if args.filewrite:
            z_utils.strToFile(resutl_context, 'BBSList', 'html')

        if status_code != '200':
            print('End Status Code:', status_code)
            try:
                sys.exit(0)
            except:
                os._exit(0)

            return status_code

        soup = BeautifulSoup(resutl_context, 'html.parser')
        findCheck = soup.find_all('div', attrs={"class": "list-row symph-row"})
        if len(findCheck) == 0:
            print('Find Check is 0')
            try:
                sys.exit(0)
            except:
                os._exit(0)
            return 400

        for list_row in soup.find_all('div', attrs={"class": "list-row symph-row"}):

            #Find Link
            list_subject = list_row.find('a', attrs={"class": "list-subject"})
            url_path_split = [x for x in re.sub(r':?service|board','',urlparse(list_subject['href']).path).split('/') if x]
            bbsclass = url_path_split[0]
            seq = int(url_path_split[1])

            #Find time
            try:
                list_time = list_row.find('div', attrs={"class": "list-time"}).find('span', attrs={"class": "timestamp"}).text
            except:
                list_time = 'None'

            db_result = 0
            if bbsclass not in ['notice', 'rule']:
                db_result = db_article_index.sqlExistCheckForStatusUpdate(bbsclass, seq, page, list_time)
                if db_result == 0:
                    countfail += 1
                else:
                    countok += 1

            sys.stdout.flush()

        item = {}
        item['seq'] = page
        item['agentid'] = socket_port
        item['workstate'] = 1
        item['resultstate'] = status_code
        item['countloop'] = callcount
        item['countok'] = countok
        item['countfail'] = countfail
        db_agent.setAgent(item)
        page = page + 1 #Page 증가
        #Continue For Loop, Don't Return.


#---------------------------------
# Tor Process Loop
def tor_loop(args, callcount):
    #Init Agent
    item = {}
    item['agentid'] = args.socket_port #init
    tor_process = None

    try:
        tor_process, socket_port = article_get_by_tor.get_tor_process(args.socket_port)

        item['agentid'] = socket_port
        item['processid'] = os.getpid()
        item['subprocessid'] = tor_process.pid
        item['countloop'] = callcount
        db_agent.initAgent(item)

        get_list(socket_port, args, callcount)

    finally:
        db_agent.logAgent(item)
        if tor_process != None:
            article_get_by_tor.kill_tor_process(tor_process)

#---------------------------------
# Batch Suit
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crawing BBS')
    parser.add_argument('-s', dest='startpage', action='store', type=int,
                       default=0,
                       help='Index Collect Start Page(po=?)')

    parser.add_argument('-p', dest='socket_port', action='store', type=int,
                       default=0,
                       help='Socket Port for TOR')

    parser.add_argument('-f', dest='filewrite', action='store_true',
                       help='Request Out to Write File')

    parser.add_argument('-t', dest='targetboard', action='store',
                       required=True, choices=['board', 'cm'],
                       help='Index Page Type')

    parser.add_argument('-y', dest='articlePeriod', action='store',
                       default=None,
                       help='Post Year')

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
            print("{}".format(sys.exc_info()[0]))
            print("{}".format(sys.exc_info()[1]))
            print("{}".format(sys.exc_info()[2]))
            print('Sleep 30sec for socket End')
            time.sleep(30)
