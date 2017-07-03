import sys
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
    for page in count(args.startpage):
        url = const_config.get_indexurl() + '?po=' + str(page)
        status_code, resutl_context = article_get_by_tor.get_article(url, socket_port, page)

        if status_code != '200':
            print('End Status Code:', status_code)
            try:
                sys.exit(0)
            except:
                os._exit(0)

            return status_code

        if args.filewrite:
            z_utils.strToFile(resutl_context, 'BBSList', 'html')

        soup = BeautifulSoup(resutl_context, 'html.parser')

        for article in soup.find_all('a', attrs={"class": "list-subject"}):
            #url_path_split= list(filter(lambda x:x,re.split('[/]',re.sub(r':?service|board','',urlparse(article['href']).path))))
            url_path_split = [x for x in re.sub(r':?service|board','',urlparse(article['href']).path).split('/') if x]
            bbsclass = url_path_split[0]
            seq = int(url_path_split[1])

            if bbsclass not in ['notice', 'rule']:
                db_article_index.sqlExistCheckForStatusUpdate(bbsclass, seq)

            # title = article.text.replace('\0','').strip()
            # print(url_path_split, title)

            # if url_path_split[0] == bbs_class:
            #     db_article_index.insertItem(int(url_path_split[1]), bbs_class, startpage, processid)
            sys.stdout.flush()



#---------------------------------
# Tor Process Loop
def tor_loop(args, callcount):

    try:
        tor_process, socket_port = article_get_by_tor.get_tor_process(args.socket_port)

        #Init Agent
        item = {}
        item['agentid'] = socket_port
        db_agent.initAgent(item)

        get_list(socket_port, args, callcount)

    finally:
        db_agent.logAgent(item)
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
            print('Sleep 30sec for socket End')
            time.sleep(30)
