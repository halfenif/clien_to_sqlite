import sys
import const_config
import article_get
import article_parse
import db_article
import article_get_by_tor

import time
from time import gmtime, strftime


def get_seq():
    seq = db_article.sqlGetMaxSeq()
    seq = seq + 1
    print('Start seq:' + str(seq))

    return seq, 0


#---------------------------------
# Test Suit
if __name__ == "__main__":
    seq, cnt_error = get_seq() #Check Seq

    try:
        if const_config.get_request_type() == "TOR":
            tor_process, socket_port = article_get_by_tor.get_tor_process()

        while True:
            url = const_config.gey_url_by_seq(seq)
            if const_config.get_request_type() == "TOR":
                status_code, resutl_context = article_get_by_tor.get_article(url, socket_port)

            if status_code == '200':
                resutl_title, resutl_body, resutl_time, result_user = article_parse.parse_article(resutl_context)
                db_article.insertItem(seq, resutl_title, resutl_body, resutl_time, result_user)
                cnt_error = 0 #Reset Error
                seq = seq + 1 #Next
            else:
                cnt_error = cnt_error + 1 #
                seq = seq + 1 #Next

                if cnt_error >= 100:
                    seq, cnt_error = get_seq() #Check Seq

                    print('Sleep:' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' : ' + str(seq))
                    time.sleep(1 * 60 * 1) #wait

            if (seq % 10) == 0:
                print('seq:' + str(seq))

            sys.stdout.flush()

    finally:
        if const_config.get_request_type() == "TOR":
            article_get_by_tor.kill_tor_process(tor_process)
