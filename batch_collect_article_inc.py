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
import article_get_by_tor

#---------------------------------
# Article Get And DB Insert Loop
def get_article(socket_port, seq, args):
    for i in count(1):
        seq += 1
        url = const_config.get_url_by_seq(seq)

        status_code, resutl_context = article_get_by_tor.get_article(url, socket_port)

        if args.filewrite:
            z_utils.strToFile(html, 'Article', 'html')

        if status_code == '200':
            result = article_parse.parse_article(resutl_context)
            result['seq'] = seq
            result['processid'] = socket_port
            db_article.insertItem(result)

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

        if args.startseq == 0:
            seq = db_article.sqlGetMaxSeq()
        else:
            seq = args.startseq

        print('Process ID:', socket_port, 'Start Seq:', seq)
        get_article(socket_port, seq, args)
    finally:
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
