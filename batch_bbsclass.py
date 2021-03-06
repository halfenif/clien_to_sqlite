import sys
import os
import const_config
import const_bbsclass
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
def get_article(socket_port, target, args, callcount):
    countok = 0
    countfail = 0
    for i, row in enumerate(target, 1):
        seq = row['seq']
        bbsclass = row['bbsclass']

        if bbsclass != '?':
            url = const_config.get_baseurl() + bbsclass + '/' + str(seq)
            status_code, resutl_context = article_get_by_tor.get_article(url, socket_port, seq)
        else:
            bFound = False
            for j, bbsclass in enumerate(const_bbsclass.get_bbsclass(),1):
                url = const_config.get_baseurl() + bbsclass + '/' + str(seq)
                status_code, resutl_context = article_get_by_tor.get_article(url, socket_port, seq)
                if status_code == '200':
                    bFound = True
                    print('Found:', j, bbsclass, url)
                    break;

            if not bFound:
                print('Not Matched:', seq)
                bbsclass = 'x' #Not Matched



        item = {}
        item['seq'] = seq
        item['agentid'] = socket_port
        item['processid'] = os.getpid()
        item['bbsclass'] = bbsclass
        item['workstate'] = 1
        item['resultstate'] = status_code

        if args.filewrite:
            z_utils.strToFile(html, 'Article', 'html')

        if status_code == '200':
            countok += 1
            result_parse = article_parse.parse_article(resutl_context, seq)
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
            print("[ {} ]                       [ {} ][ {} ][ {}/{} Called ]".format(time.strftime('%x %X', time.localtime()), socket_port, format(seq,','), i, (callcount * len(target) + i )))
            sys.stdout.flush()

#---------------------------------
# Tor Process Loop
def tor_loop(args, callcount):
    tor_process = None
    #Init Agent
    item = {}
    item['agentid'] = args.socket_port

    try:
        tor_process, socket_port = article_get_by_tor.get_tor_process(args.socket_port)
        item['agentid'] = socket_port

        db_agent.initAgent(item)

        #Make Target
        target = db_article_index.getTargetForBbsclass(item)

        if len(target) == 0:
            print('END: Target is Empty!!')
            return
            # try:
            #     sys.exit(0)
            # except:
            #     os._exit(0)


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
    parser = argparse.ArgumentParser(description='Crawing Article')
    parser.add_argument('-s', dest='startseq', action='store', type=int,
                       default=0,
                       help='Article Start Sequqnce')

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
