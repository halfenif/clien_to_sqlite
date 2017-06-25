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
# Article Get And DB Insert Loop
def get_article(socket_port, target, args):
    countok = 0
    countfail = 0
    for i, seq in enumerate(target, 1):
        url = const_config.get_url_by_seq(seq)

        status_code, resutl_context = article_get_by_tor.get_article(url, socket_port)

        item = {}
        item['seq'] = seq
        item['agentid'] = socket_port
        item['processid'] = os.getpid()
        item['bbsclass'] = const_config.get_bbs_class()
        item['workstate'] = 1
        item['resultstate'] = status_code

        if args.filewrite:
            z_utils.strToFile(html, 'Article', 'html')


        if status_code == '200':
            countok += 1
            result_parse = article_parse.parse_article(resutl_context)
            item.update(result_parse)
            db_article.insertItem(item)
        else:
            countfail += 1

        #Result update
        item['countok'] = countok
        item['countfail'] = countfail

        db_article_index.sqlUpdate(item)
        db_agent.setAgent(item)

        if (i % 10) == 0:
            print("[ {} ][ {} Called ]".format(time.strftime('%x %X', time.localtime()), i))

        if seq == 0:
            print("[ {} ][ {} Called ][ Seq is 0. END ]".format(time.strftime('%x %X', time.localtime()), i))
            return

        sys.stdout.flush()

#---------------------------------
# Tor Process Loop
def tor_loop(args):

    try:
        tor_process, socket_port = article_get_by_tor.get_tor_process()

        #Init Agent
        item = {}
        item['agentid'] = socket_port
        db_agent.initAgent(item)

        #Make Target
        target = db_article_index.getTarget(item)

        if len(target) == 0:
            print('END: Target is Empty!!')
            try:
                sys.exit(0)
            except:
                os._exit(0)


        get_article(socket_port, target, args)
    finally:
        db_agent.logAgent(item)
        article_get_by_tor.kill_tor_process(tor_process)

#---------------------------------
# Main Suit
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crawing Article')
    parser.add_argument('-s', dest='startseq', action='store', type=int,
                       default=0,
                       help='Article Start Sequqnce')


    parser.add_argument('-f', dest='filewrite', action='store_true',
                       help='Request Out to Write File')

    #Parse Argument
    args = parser.parse_args()

    while True:
        try:
            tor_loop(args)
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
